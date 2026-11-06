#!/usr/bin/env python3
"""Teacher-generated multidomain SFT on the existing 500M checkpoint, then paired holdout."""
from __future__ import annotations
import gc, hashlib, json, os, random, re, time
from dataclasses import replace
from pathlib import Path
import torch
from llama_cpp import Llama
from ronin.config import ModelConfig, get_profile
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer

ROOT=Path("reports/multidomain")
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

def extract_json_object(content:str)->dict:
    """Extract the first complete JSON object despite fences or leading prose."""
    if isinstance(content,list):
        content="".join(part.get("text","") for part in content if isinstance(part,dict))
    if not isinstance(content,str):
        raise ValueError("Instructor content is not text")
    decoder=json.JSONDecoder()
    for offset,char in enumerate(content):
        if char!="{":
            continue
        try:
            value,_=decoder.raw_decode(content[offset:])
        except json.JSONDecodeError:
            continue
        if isinstance(value,dict):
            return value
    raise ValueError("Instructor did not return a complete JSON object")

def teacher_call(teacher:Llama,domain:str,count:int,batch_no:int)->list[dict]:
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
Devuelve un objeto JSON con la clave examples. No añadas Markdown.
"""
    result=teacher.create_chat_completion(
        messages=[{"role":"system","content":system},{"role":"user","content":user}],
        temperature=0.55,top_p=0.9,max_tokens=2200,
        response_format={"type":"json_object"})
    parsed=extract_json_object(result["choices"][0]["message"]["content"])
    examples=parsed.get("examples",[])
    if not isinstance(examples,list):
        raise ValueError("Instructor JSON has no examples array")
    return examples

def valid_teacher_row(item:object,domain:str)->dict|None:
    if not isinstance(item,dict):
        return None
    question=str(item.get("question","")).strip()
    answer=str(item.get("answer","")).strip()
    explanation=str(item.get("explanation","")).strip()
    if not (20<=len(question)<=180 and 1<=len(answer)<=100 and 8<=len(explanation)<=180):
        return None
    return {"domain":domain,"question":question,"answer":answer,"explanation":explanation,
            "teacher":"SoAIHQ/Qwen3.5-4B-GGUF Q4_K_M",
            "verification":"teacher_generated_format_length_and_uniqueness_only"}

def load_resumable_dataset(output:Path)->tuple[list[dict],set[str],dict[str,int]]:
    accepted=[]; seen=set(); counts={domain:0 for domain in DOMAINS}
    if not output.exists():
        return accepted,seen,counts
    lines=output.read_bytes().splitlines(keepends=True)
    valid_lines=[]
    for index,line in enumerate(lines):
        try:
            row=json.loads(line.decode("utf-8"))
            domain=row.get("domain")
            if domain not in DOMAINS:
                raise ValueError(f"Unknown domain in existing teacher JSONL: {domain}")
            normalized=re.sub(r"\\s+"," ",str(row.get("question","")).casefold())
            if not normalized or normalized in seen:
                continue
            if not (row.get("answer") and row.get("explanation")):
                raise ValueError(f"Incomplete existing teacher row at line {index+1}")
            if counts[domain]>=COUNTS[domain]:
                continue
            seen.add(normalized); counts[domain]+=1; accepted.append(row); valid_lines.append(line)
        except (UnicodeDecodeError,json.JSONDecodeError):
            if index!=len(lines)-1 or line.endswith(b"\\n"):
                raise ValueError(f"Corrupt teacher JSONL at line {index+1}; refusing unsafe resume")
            break
    if len(valid_lines)!=len(lines):
        temporary=output.with_suffix(".jsonl.recovered")
        temporary.write_bytes(b"".join(valid_lines))
        temporary.replace(output)
    return accepted,seen,counts

def write_manifest(accepted:list[dict])->None:
    counts={domain:sum(row["domain"]==domain for row in accepted) for domain in DOMAINS}
    manifest={"schema":"heretic-teacher-multidomain-v2","examples":len(accepted),"domain_counts":counts,
        "teacher":"SoAIHQ/Qwen3.5-4B-GGUF","teacher_quantization":"Q4_K_M",
        "teacher_sha256":"2ebe6eb67cb92adeffc7073c48dd4e3baf79465ac650793dc751cad2b29cf219",
        "seed":SEED,"generation_runtime":"llama-cpp-python in-process CPU; no HTTP server",
        "quality_note":"Format, length and uniqueness checks only; teacher answers are not independently verified.",
        "resume":"Accepted JSONL rows are fsync-persisted individually and reused on restart.",
        "holdout_separation":"The deterministic holdout is generated locally after teacher generation and is never sent to the instructor."}
    target=ROOT/"teacher-dataset-manifest.json"; temporary=target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    temporary.replace(target)

def build_teacher_dataset(teacher_path:Path)->list[dict]:
    ROOT.mkdir(parents=True,exist_ok=True)
    output=ROOT/"teacher-multidomain-1000.jsonl"
    accepted,seen,counts=load_resumable_dataset(output)
    print(f"resume: {sum(counts.values())}/1000 examples already persisted",flush=True)
    if sum(counts.values())==1000:
        if any(counts[d]!=COUNTS[d] for d in DOMAINS):
            raise AssertionError(f"invalid resumed domain distribution: {counts}")
        write_manifest(accepted)
        return accepted
    teacher=Llama(model_path=str(teacher_path),n_ctx=4096,n_threads=4,n_threads_batch=4,
                  n_batch=512,n_gpu_layers=0,use_mmap=True,verbose=False)
    calls=0
    try:
        for domain,target in COUNTS.items():
            while counts[domain]<target:
                requested=min(10,target-counts[domain]); calls+=1
                if calls>300:
                    raise RuntimeError(f"Teacher generation exceeded 300 calls; accepted={len(accepted)}")
                batch=[]; last_error=None
                for attempt in range(3):
                    try:
                        batch=teacher_call(teacher,domain,requested,calls)
                        break
                    except Exception as exc:
                        last_error=exc
                        print(f"teacher retry {attempt+1}/3 for {domain}: {exc}",flush=True)
                        time.sleep(2*(attempt+1))
                else:
                    raise RuntimeError(f"Teacher batch failed for {domain}: {last_error}")
                added=0
                with output.open("a",encoding="utf-8") as handle:
                    for item in batch:
                        row=valid_teacher_row(item,domain)
                        if row is None:
                            continue
                        key=re.sub(r"\\s+"," ",row["question"].casefold())
                        if key in seen or counts[domain]>=target:
                            continue
                        row["id"]=f"{domain}-{counts[domain]+1:04d}"
                        handle.write(json.dumps(row,ensure_ascii=False)+"\\n")
                        handle.flush(); os.fsync(handle.fileno())
                        accepted.append(row); seen.add(key); counts[domain]+=1; added+=1
                print(f"accepted {domain}: {counts[domain]}/{target} (+{added}; total {len(accepted)}/1000)",flush=True)
                if added==0:
                    time.sleep(1)
        if len(accepted)!=1000 or any(counts[d]!=COUNTS[d] for d in DOMAINS):
            raise AssertionError(f"expected exact 1000-example domain balance, got {counts}")
        write_manifest(accepted)
        return accepted
    finally:
        teacher.close()
        del teacher
        gc.collect()

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
    ROOT.mkdir(parents=True,exist_ok=True)
    teacher_path=Path("instructor/Qwen3.5-4B-Q4_K_M.gguf")
    if not teacher_path.is_file():
        matches=list(Path("instructor").rglob("Qwen3.5-4B-Q4_K_M.gguf"))
        if not matches:
            raise FileNotFoundError("Verified Qwen3.5-4B GGUF instructor was not found")
        teacher_path=matches[0]
    rows=build_teacher_dataset(teacher_path)
    gc.collect()
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
                           "One run and a synthetic holdout do not establish general multidomain reasoning."]}
    (ROOT/"experiment-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
