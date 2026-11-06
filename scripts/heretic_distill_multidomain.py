#!/usr/bin/env python3
"""Teacher-generated multidomain SFT on the existing 500M checkpoint, then paired holdout."""
from __future__ import annotations
import hashlib, json, os, random, re, signal, time, urllib.request
from dataclasses import replace
from pathlib import Path
import torch
from ronin.config import ModelConfig, get_profile
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer

ROOT=Path("reports/multidomain")
TEACHER_URL="http://127.0.0.1:8080/v1/chat/completions"
DOMAINS={"mathematics":"matemáticas y resolución cuantitativa","programming":"programación, lectura de código y algoritmos","logic":"lógica formal, deducción y restricciones","natural_science":"ciencias naturales y explicación causal","language":"lengua española, gramática y significado","interdisciplinary":"problemas interdisciplinares y unidades"}
COUNTS={"mathematics":167,"programming":167,"logic":167,"natural_science":167,"language":166,"interdisciplinary":166}
SEED=20261106
STUDENT_INPUT=Path("incoming/student-500m-step-00000100.pt")
LONG_METHOD_INPUT=Path("incoming/ronin-drosophila-main.pt")
STUDENT_OUTPUT=ROOT/"student-500m-multidomain-distilled.pt"

def sha256_file(path:Path)->str:
    digest=hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda:handle.read(1024*1024),b""): digest.update(chunk)
    return digest.hexdigest()

def teacher_call(domain:str,count:int,batch_no:int)->list[dict]:
    system=("Eres un instructor experto que crea ejemplos breves y verificables para enseñar razonamiento multidominio a un modelo pequeño. "
            "Escribe exclusivamente en español. No inventes citas ni datos actuales. Prioriza problemas autocontenidos, solución correcta "
            "y explicación breve. No incluyas cadena de pensamiento privada.")
    user=f"""
Genera exactamente {count} ejemplos NUEVOS del dominio {domain} ({DOMAINS[domain]}).
Lote {batch_no}. Cada ejemplo debe tener:
- question: pregunta autocontenida y breve, idealmente menos de 65 caracteres.
- answer: respuesta final inequívoca, idealmente menos de 35 caracteres.
- explanation: justificación verificable en una frase de menos de 65 caracteres.
Evita repetir preguntas, usa variedad real y dificultad introductoria/intermedia.
Devuelve solo un objeto JSON con esta forma:
{{"examples":[{{"question":"...","answer":"...","explanation":"..."}}]}}
No añadas Markdown ni texto fuera del JSON.
"""
    payload={"model":"qwen3.5-4b-instructor","messages":[{"role":"system","content":system},{"role":"user","content":user}],
             "temperature":0.65,"top_p":0.9,"max_tokens":1800,"response_format":{"type":"json_object"}}
    request=urllib.request.Request(TEACHER_URL,data=json.dumps(payload,ensure_ascii=False).encode("utf-8"),
                                   headers={"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(request,timeout=900) as response: result=json.loads(response.read().decode("utf-8"))
    content=result["choices"][0]["message"]["content"]
    if isinstance(content,list): content="".join(part.get("text","") for part in content if isinstance(part,dict))
    try: parsed=json.loads(content)
    except json.JSONDecodeError:
        match=re.search(r"\{.*\}",content,flags=re.DOTALL)
        if not match: raise ValueError("Instructor did not return a JSON object")
        parsed=json.loads(match.group(0))
    examples=parsed.get("examples",[])
    if not isinstance(examples,list): raise ValueError("Instructor JSON has no examples array")
    return examples

def build_teacher_dataset()->list[dict]:
    ROOT.mkdir(parents=True,exist_ok=True)
    output=ROOT/"teacher-multidomain-1000.jsonl"
    accepted=[]; seen=set(); calls=0
    for domain,target in COUNTS.items():
        domain_count=0
        while domain_count<target:
            requested=min(10,target-domain_count); calls+=1
            if calls>160: raise RuntimeError(f"Teacher generation exceeded 160 calls; accepted={len(accepted)}")
            batch=[]; last_error=None
            for attempt in range(3):
                try: batch=teacher_call(domain,requested,calls); break
                except Exception as exc: last_error=exc; time.sleep(2*(attempt+1))
            else: raise RuntimeError(f"Teacher batch failed for {domain}: {last_error}")
            for item in batch:
                if not isinstance(item,dict): continue
                question=str(item.get("question","")).strip()
                answer=str(item.get("answer","")).strip()
                explanation=str(item.get("explanation","")).strip()
                key=re.sub(r"\s+"," ",question.casefold())
                if not (20<=len(question)<=180 and 1<=len(answer)<=100 and 8<=len(explanation)<=180): continue
                if key in seen: continue
                seen.add(key)
                accepted.append({"id":f"{domain}-{domain_count+1:04d}","domain":domain,"question":question,
                                 "answer":answer,"explanation":explanation,"teacher":"SoAIHQ/Qwen3.5-4B-GGUF Q4_K_M",
                                 "verification":"teacher_generated_format_and_uniqueness_checks_only"})
                domain_count+=1
                if domain_count>=target: break
        print(f"accepted {domain}: {domain_count}/{target}",flush=True)
    with output.open("w",encoding="utf-8") as handle:
        for item in accepted: handle.write(json.dumps(item,ensure_ascii=False)+"\n")
    if len(accepted)!=1000: raise AssertionError(f"expected 1000 teacher examples, got {len(accepted)}")
    counts={domain:sum(row["domain"]==domain for row in accepted) for domain in DOMAINS}
    (ROOT/"teacher-dataset-manifest.json").write_text(json.dumps({
        "schema":"heretic-teacher-multidomain-v1","examples":len(accepted),"domain_counts":counts,
        "teacher":"SoAIHQ/Qwen3.5-4B-GGUF","teacher_quantization":"Q4_K_M",
        "teacher_sha256":"2ebe6eb67cb92adeffc7073c48dd4e3baf79465ac650793dc751cad2b29cf219",
        "seed":SEED,"quality_note":"Format, length and duplicate checks only; teacher answers are not independently verified.",
        "holdout_separation":"The deterministic holdout is generated locally after teacher generation and is never sent to the instructor."
    },ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return accepted

def encode_sft_rows(rows:list[dict],context:int)->tuple[torch.Tensor,torch.Tensor]:
    xs=[]; ys=[]
    for row in rows:
        target=f" {row['answer']}\nR: {row['explanation']}".encode("utf-8")
        if len(target)>context-12:
            answer=row["answer"].encode("utf-8")
            if len(answer)>context-24: continue
            explanation=row["explanation"].encode("utf-8")[:context-len(answer)-16]
            target=b" "+answer+b"\nR: "+explanation
        prefix=f"Q: {row['question']}\nA:".encode("utf-8")
        max_prefix=context-len(target)-1
        if max_prefix<8: continue
        prefix=prefix[:max_prefix]
        sequence=(prefix+target+b"\n")[:context]
        x=torch.zeros(context,dtype=torch.long); y=torch.full((context,),-100,dtype=torch.long)
        values=list(sequence)
        if len(values)<2: continue
        x[:len(values)-1]=torch.tensor(values[:-1],dtype=torch.long)
        first_target=len(prefix)-1
        y[first_target:len(values)-1]=torch.tensor(values[len(prefix):],dtype=torch.long)
        xs.append(x); ys.append(y)
    if len(xs)<900: raise RuntimeError(f"too few usable SFT rows after context packing: {len(xs)}")
    return torch.stack(xs),torch.stack(ys)

def train_student(rows:list[dict])->dict:
    torch.set_num_threads(4); torch.set_num_interop_threads(1)
    checkpoint=torch.load(STUDENT_INPUT,map_location="cpu",weights_only=False)
    if int(checkpoint.get("step",-1))!=100: raise ValueError("Student checkpoint is not the completed 100-step checkpoint")
    config_data=checkpoint.get("model_config")
    if not isinstance(config_data,dict): raise ValueError("Student checkpoint has no model_config")
    config=ModelConfig(**config_data)
    if config.context_length!=128: raise ValueError(f"Expected original 128-byte context, got {config.context_length}")
    model=RoninLM(config); model.load_state_dict(checkpoint["model"],strict=True)
    del checkpoint
    if model.parameter_count!=500_102_144: raise ValueError(f"Unexpected student parameter count: {model.parameter_count}")
    x_all,y_all=encode_sft_rows(rows,config.context_length)
    rng=random.Random(SEED); torch.manual_seed(SEED)
    optimizer=torch.optim.AdamW(model.parameters(),lr=1e-5,weight_decay=0.01)
    order=list(range(len(x_all))); rng.shuffle(order)
    batch_size=2; steps=(len(order)+batch_size-1)//batch_size
    losses=[]; model.train(); started=time.perf_counter()
    for step in range(steps):
        indices=order[step*batch_size:(step+1)*batch_size]
        inputs=x_all[indices]; targets=y_all[indices]
        optimizer.zero_grad(set_to_none=True); _,loss=model(inputs,targets)
        if loss is None or not torch.isfinite(loss): raise FloatingPointError(f"non-finite distillation loss at step {step}")
        loss.backward(); grad_norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
        if not torch.isfinite(grad_norm): raise FloatingPointError(f"non-finite gradient at step {step}")
        lr=1e-5*min(1.0,(step+1)/20)
        for group in optimizer.param_groups: group["lr"]=lr
        optimizer.step(); losses.append(float(loss.detach()))
        if (step+1)%25==0: print(f"distillation step {step+1}/{steps} loss={losses[-1]:.5f}",flush=True)
    elapsed=time.perf_counter()-started; model.eval()
    torch.save({"model":model.state_dict(),"model_config":config.__dict__,"step":600,"parameter_count":model.parameter_count,
                "seed":SEED,"initialization":"continued_from_student_500m_step_100",
                "teacher":"SoAIHQ/Qwen3.5-4B-GGUF Q4_K_M","distillation_steps":steps,"optimizer_state_included":False},STUDENT_OUTPUT)
    return {"checkpoint":str(STUDENT_OUTPUT),"checkpoint_sha256":sha256_file(STUDENT_OUTPUT),"parameters":model.parameter_count,
            "starting_step":100,"ending_step":600,"distillation_steps":steps,"examples_seen":len(order),"batch_size":batch_size,"sft_rows":len(x_all),
            "initial_loss":losses[0],"final_loss":losses[-1],"training_seconds":elapsed,
            "interpretation":"Training loss is not a capability or generalization result."}

def holdout_rows()->list[dict]:
    """Deterministic local tasks; never queried from the instructor."""
    rows=[]
    nouns=[("libro","libros"),("árbol","árboles"),("canción","canciones"),("papel","papeles"),
           ("flor","flores"),("reloj","relojes"),("animal","animales"),("luz","luces"),
           ("ciudad","ciudades"),("mesa","mesas")]
    for i in range(10):
        a,b,c=7+i*3,2+(i%5),5+i*2
        rows.append({"domain":"mathematics","question":f"Calcula {a} por {b} más {c}. Solo el número.","answer":str(a*b+c)})
        values=list(range(i+1,i+6))
        rows.append({"domain":"programming","question":f"En Python, ¿cuánto vale len({values})? Solo el número.","answer":str(len(values))})
        names=("Alba","Bruno","Celia")
        first,second,third=(names[(i+j)%3] for j in range(3))
        rows.append({"domain":"logic","question":f"{first} es mayor que {second}, y {second} que {third}. ¿Quién es menor? Solo el nombre.","answer":third})
        distance,seconds=(i+2)*12,i+2
        rows.append({"domain":"natural_science","question":f"Un móvil recorre {distance} metros en {seconds} segundos. ¿Velocidad en m/s? Solo el número.","answer":str(distance//seconds)})
        singular,plural=nouns[i]
        rows.append({"domain":"language","question":f"Escribe en plural: {singular}. Solo la palabra.","answer":plural})
        kilograms=i+1
        rows.append({"domain":"interdisciplinary","question":f"Convierte {kilograms} kilogramos a gramos. Solo el número.","answer":str(kilograms*1000)})
    return rows

def normalize_answer(value:str)->str:
    value=value.splitlines()[0] if value.splitlines() else value
    value=value.strip().casefold()
    value=re.sub(r"^(la respuesta es|respuesta:|answer:)","",value).strip()
    return re.sub(r"\s+"," ",value).strip(" \t\r\n.,;:!?¿¡\"'()[]{}")

@torch.inference_mode()
def generate_answer(model:RoninLM,question:str,max_new_tokens:int=32)->str:
    tokenizer=ByteTokenizer(); prompt=tokenizer.encode(f"Q: {question}\nA:")
    generated=[]; model.eval()
    for _ in range(max_new_tokens):
        context=(prompt+generated)[-model.config.context_length:]
        ids=torch.tensor([context],dtype=torch.long)
        logits=model.forward_last_logits(ids,torch.tensor([len(context)-1],dtype=torch.long))
        token=int(torch.argmax(logits[0]).item())
        if token==10: break
        generated.append(token)
    return tokenizer.decode(generated).strip()

def load_long_method_model()->RoninLM:
    base_config,_=get_profile("tiny"); long_config=replace(base_config,d_ff=12_700)
    model=RoninLM(long_config)
    checkpoint=torch.load(LONG_METHOD_INPUT,map_location="cpu",weights_only=False)
    state=checkpoint.get("model",checkpoint) if isinstance(checkpoint,dict) else None
    if not isinstance(state,dict): raise ValueError("Long-method checkpoint has no model state_dict")
    model.load_state_dict(state,strict=True)
    if model.parameter_count!=100_900_160: raise ValueError(f"Unexpected long-method parameter count: {model.parameter_count}")
    return model

def evaluate_pair(student:RoninLM)->dict:
    tasks=holdout_rows(); baseline=load_long_method_model()
    results={"holdout_schema":"heretic-independent-multidomain-holdout-v1","teacher_saw_holdout":False,"questions":len(tasks),"models":{}}
    for name,model in (("ronin_ia_long_method_100_9m",baseline),("heretic_student_500m_distilled",student)):
        per_domain={}; details=[]; correct_total=0
        for index,task in enumerate(tasks):
            prediction=generate_answer(model,task["question"])
            correct=normalize_answer(prediction)==normalize_answer(task["answer"])
            correct_total+=int(correct)
            per_domain.setdefault(task["domain"],{"correct":0,"total":0})
            per_domain[task["domain"]]["correct"]+=int(correct); per_domain[task["domain"]]["total"]+=1
            details.append({"index":index,"domain":task["domain"],"question":task["question"],
                            "expected":task["answer"],"prediction":prediction,"correct":correct})
            if (index+1)%10==0: print(f"{name}: evaluated {index+1}/{len(tasks)}",flush=True)
        results["models"][name]={"correct":correct_total,"total":len(tasks),"accuracy":correct_total/len(tasks),
                                 "by_domain":per_domain,"details":details}
        del model
    results["comparison"]={"accuracy_delta_percentage_points":(
        results["models"]["heretic_student_500m_distilled"]["accuracy"]-
        results["models"]["ronin_ia_long_method_100_9m"]["accuracy"])*100,
        "decision":"MEASURED_ON_THIS_SMALL_SYNTHETIC_HOLDOUT_ONLY"}
    (ROOT/"paired-holdout-results.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return results

def main()->None:
    ROOT.mkdir(parents=True,exist_ok=True); rows=build_teacher_dataset()
    # Release the 4B instructor from RAM before loading the 500M student and AdamW state.
    pid_file=Path("llama-server.pid")
    if pid_file.is_file():
        try: os.kill(int(pid_file.read_text().strip()),signal.SIGTERM)
        except (ProcessLookupError,ValueError): pass
    train_report=train_student(rows)
    checkpoint=torch.load(STUDENT_OUTPUT,map_location="cpu",weights_only=False)
    config=ModelConfig(**checkpoint["model_config"]); student=RoninLM(config)
    student.load_state_dict(checkpoint["model"],strict=True); student.eval()
    holdout=evaluate_pair(student)
    report={"experiment":"heretic-multidomain-distillation-cycle-001","teacher_examples":len(rows),
            "domain_counts":{d:sum(r["domain"]==d for r in rows) for d in DOMAINS},"training":train_report,
            "holdout":{"questions":holdout["questions"],"teacher_saw_holdout":False,
                       "models":{name:{"correct":v["correct"],"total":v["total"],"accuracy":v["accuracy"],"by_domain":v["by_domain"]}
                                 for name,v in holdout["models"].items()},"comparison":holdout["comparison"]},
            "limitations":["Teacher examples pass structural, length and duplicate checks, not independent semantic verification.",
                           "Holdout is a small deterministic synthetic diagnostic, not an official benchmark.",
                           "Student context remains 128 bytes; tokenizer and architecture are unchanged.",
                           "One run and a small holdout do not establish general multidomain reasoning."]}
    (ROOT/"experiment-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
