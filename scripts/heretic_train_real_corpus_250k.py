#!/usr/bin/env python3
"""Chunked 500M continuation on exact real RONIN-IA train artifacts."""
from __future__ import annotations
import argparse, gzip, hashlib, json, random, re, time, zipfile
from pathlib import Path
import numpy as np
import torch
from ronin.config import ModelConfig
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer

CONTEXT=128
BATCH=2
SEED=20261106
TARGET=250000
OUT=Path("out")
def sha256(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def add_jsonl(zf,name,key,store):
    count=0
    opener=gzip.open if name.endswith(".gz") else open
    with zf.open(name) as raw:
        import io
        payload=gzip.GzipFile(fileobj=raw) if name.endswith(".gz") else raw
        stream=io.TextIOWrapper(payload,encoding="utf-8")
        for line in stream:
            if not line.strip(): continue
            row=json.loads(line); value=row.get(key,"")
            if isinstance(value,str) and len(value.encode("utf-8"))>=25:
                store.append(value); count+=1
    return count

def build_corpus(path,audit_path):
    groups={}
    with zipfile.ZipFile(path) as z:
        manifest=json.loads(z.read("IMPORT-MANIFEST.json"))
        if manifest.get("records_staged")!=286464: raise RuntimeError("RONIN-IA artifact count mismatch")
        if manifest.get("active_training_authorized") is not False: raise RuntimeError("Unexpected import manifest state")
        covost=[]; mathlib=[]; science=[]
        add_jsonl(z,"covost2-cc0/train.jsonl.gz","text",covost)
        add_jsonl(z,"mathlib4-apache/documents.train.jsonl.gz","text",mathlib)
        add_jsonl(z,"scienceverse-ccby/documents.train.jsonl","text",science)
        literature=z.read("literature-es/train.txt").decode("utf-8")
        lit=[p.strip() for p in literature.split("\n\n") if len(p.strip())>=40]
        nasa=z.read("nasa-ntrs-file-reviewed/train.txt").decode("utf-8")
        papers=[z.read(n).decode("utf-8") for n in z.namelist()
                if n.startswith("ronin-authored-papers/") and n.endswith(".md")]
    groups={"covost2":covost,"mathlib4":mathlib,"scienceverse":science,
            "literature_es":lit,"nasa_ntrs":([nasa] if len(nasa.encode("utf-8"))>=40 else []),
            "ronin_papers":papers}
    audit=json.loads(Path(audit_path).read_text())
    if audit.get("training_authorized") is not True: raise RuntimeError("Audit report does not authorize cleaned corpus")
    expected=audit.get("source_counts",{})
    audit_order=("covost2","mathlib4","scienceverse","literature","nasa","papers")
    mapping={"literature":"literature_es","nasa":"nasa_ntrs","papers":"ronin_papers"}
    ordered=[]
    for source in audit_order:
        key=mapping.get(source,source)
        docs=groups[key]
        if len(docs)!=expected.get(source): raise RuntimeError(f"{source}: audit counted {expected.get(source)}, loader got {len(docs)}")
        ordered.extend((source,doc) for doc in docs)
    if len(ordered)!=audit.get("documents_audited"): raise RuntimeError("Global audit document index mismatch")
    plan=audit.get("deduplication_plan",{})
    if plan.get("near_duplicate_pair_list_complete") is not True or plan.get("exact_duplicate_records_covered") is not True:
        raise RuntimeError("Duplicate exclusion plan is incomplete")
    excluded=set(plan.get("excluded_global_indices",[]))
    if any(i<0 or i>=len(ordered) for i in excluded): raise RuntimeError("Invalid duplicate exclusion index")
    clean={name:[] for name in groups}
    for index,(source,doc) in enumerate(ordered):
        if index in excluded: continue
        clean[mapping.get(source,source)].append(doc)
    arrays={}
    for name,docs in clean.items():
        payload=b"\n\n".join(x.encode("utf-8") for x in docs)
        if len(payload)<1024: raise RuntimeError(f"Corpus source unexpectedly small: {name}")
        arrays[name]=np.frombuffer(payload,dtype=np.uint8)
    counts={k:len(v) for k,v in clean.items()}
    info={"source_documents_before_dedup":expected,"source_documents_after_dedup":counts,
          "audited_documents_before_dedup":len(ordered),"duplicate_records_excluded":len(excluded),
          "audited_documents_after_dedup":len(ordered)-len(excluded),
          "source_bytes":{k:int(v.nbytes) for k,v in arrays.items()},
          "total_bytes":sum(int(v.nbytes) for v in arrays.values()),
          "sources":["CoVoST2 CC0 translation-only","Mathlib4 Apache-2.0","ScienceVerse per-document CC-BY/CC0",
                    "Spanish public-domain literature train","NASA file-reviewed train","owner-authorized Papers internal train"],
          "excluded":["validation/test/holdout","20,000 unreviewed open-source candidates","Drosophila procedural synthetic rows",
                     "exact and SimHash near-duplicate endpoints from the signed audit plan"]}
    return arrays,info

def holdout_rows():
    rows=[]
    plurals=[("lápiz","lápices"),("pez","peces"),("luz","luces"),("joven","jóvenes"),
             ("rubí","rubíes"),("régimen","regímenes"),("carácter","caracteres"),
             ("espécimen","especímenes"),("sofá","sofás"),("menú","menús"),
             ("bambú","bambúes"),("crisis","crisis"),("lunes","lunes"),("tórax","tórax"),
             ("análisis","análisis"),("álbum","álbumes"),("examen","exámenes"),
             ("compás","compases"),("raíz","raíces"),("canción","canciones")]
    names=("Alba","Bruno","Celia","Diego","Eva","Fabio","Gala","Hugo")
    for i in range(20):
        a=i+4; b=(i%5)+2; c=(i%4)+1
        rows.append({"domain":"mathematics","question":f"Calcula ({a} + {b}) por {c}, menos {i}. Solo el número.","answer":str((a+b)*c-i)})
        values=[i+1,i+2,i+3]
        rows.append({"domain":"programming","question":f"En Python, ¿qué vale sum({values}) - len({values})? Solo número.","answer":str(sum(values)-len(values))})
        order=[names[(i+j)%len(names)] for j in range(4)]
        rows.append({"domain":"logic","question":f"{order[0]} va antes que {order[1]}, {order[1]} antes que {order[2]} y {order[2]} antes que {order[3]}. ¿Quién va último?","answer":order[3]})
        volume=(i%5)+1; density=i+2
        rows.append({"domain":"natural_science","question":f"Una muestra tiene {volume*density} g y ocupa {volume} cm3. ¿Densidad en g/cm3? Solo número.","answer":str(density)})
        singular,plural=plurals[i]
        rows.append({"domain":"language","question":f"Escribe el plural de «{singular}». Solo la palabra.","answer":plural})
        amount=i+1
        if i<7: q=f"Convierte {amount} kg a gramos. Solo número."; ans=str(amount*1000)
        elif i<14: q=f"Convierte {amount} litros a mililitros. Solo número."; ans=str(amount*1000)
        else: q=f"Convierte {amount} horas a minutos. Solo número."; ans=str(amount*60)
        rows.append({"domain":"interdisciplinary","question":q,"answer":ans})
    return rows

def normalize(s):
    s=s.splitlines()[0] if s.splitlines() else s
    s=re.sub(r"^(la respuesta es|respuesta:|answer:)","",s.strip().casefold()).strip()
    return re.sub(r"\s+"," ",s).strip(" \t\r\n.,;:!?¿¡\"'()[]{}")

@torch.inference_mode()
def predict(model,question):
    tok=ByteTokenizer(); ids=tok.encode(f"Q: {question}\nA:"); generated=[]
    model.eval()
    for _ in range(32):
        context=(ids+generated)[-model.config.context_length:]
        x=torch.tensor([context],dtype=torch.long)
        logits=model.forward_last_logits(x,torch.tensor([len(context)-1],dtype=torch.long))
        nxt=int(torch.argmax(logits[0]).item())
        if nxt==10: break
        generated.append(nxt)
    return tok.decode(generated).strip()

def evaluate(model):
    tasks=holdout_rows(); details=[]; domains={}
    for i,t in enumerate(tasks):
        pred=predict(model,t["question"]); ok=normalize(pred)==normalize(t["answer"])
        d=domains.setdefault(t["domain"],{"correct":0,"total":0})
        d["correct"]+=int(ok); d["total"]+=1
        details.append({"index":i,**t,"prediction":pred,"correct":ok})
    correct=sum(x["correct"] for x in details)
    return {"correct":correct,"total":len(details),"accuracy":correct/len(details),
            "by_domain":domains,"details":details}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--start-step",type=int,required=True)
    p.add_argument("--steps",type=int,required=True)
    p.add_argument("--resume",action="store_true")
    a=p.parse_args()
    OUT.mkdir(exist_ok=True)
    torch.set_num_threads(4); torch.set_num_interop_threads(1)
    corpus,corpus_info=build_corpus(Path("incoming/ronin-ia-train.zip"),Path("incoming/GLOBAL-CORPUS-AUDIT.json"))
    if a.resume:
        ckpt=torch.load("incoming/checkpoint.pt",map_location="cpu",weights_only=False)
        if int(ckpt["step"])!=a.start_step: raise RuntimeError("Resume checkpoint step mismatch")
        config=ModelConfig(**ckpt["model_config"]); model=RoninLM(config)
        model.load_state_dict(ckpt["model"],strict=True)
        optimizer=torch.optim.AdamW(model.parameters(),lr=1e-5,weight_decay=0.01)
        if "optimizer_state_dict" not in ckpt: raise RuntimeError("Optimizer state missing from continuation checkpoint")
        optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        before=json.loads(Path("incoming/holdout-before.json").read_text())
        previous_losses=ckpt.get("loss_tail",[])
        seed=int(ckpt.get("seed",SEED))
    else:
        ckpt=torch.load("incoming/student-step-600.pt",map_location="cpu",weights_only=False)
        if int(ckpt.get("step",-1))!=600: raise RuntimeError("Expected distilled 500M step-600 checkpoint")
        config=ModelConfig(**ckpt["model_config"]); model=RoninLM(config)
        model.load_state_dict(ckpt["model"],strict=True)
        optimizer=torch.optim.AdamW(model.parameters(),lr=1e-5,weight_decay=0.01)
        seed=SEED; previous_losses=[]
        before=evaluate(model)
        Path("out/holdout-before.json").write_text(json.dumps(before,ensure_ascii=False,indent=2)+"\n")
    if model.parameter_count!=500102144: raise RuntimeError(f"Unexpected parameter count {model.parameter_count}")
    if a.start_step+ a.steps>TARGET: raise RuntimeError("Chunk exceeds target step")
    rng=random.Random(seed+a.start_step)
    names=list(corpus); weights=[len(corpus[n])**0.5 for n in names]
    losses=[]; started=time.perf_counter(); model.train()
    for local in range(a.steps):
        xs=[]; ys=[]
        for _ in range(BATCH):
            source=rng.choices(names,weights=weights,k=1)[0]; buf=corpus[source]
            start=rng.randrange(0,len(buf)-CONTEXT-1)
            seq=buf[start:start+CONTEXT+1].astype(np.int64,copy=False)
            xs.append(seq[:-1]); ys.append(seq[1:])
        x=torch.from_numpy(np.stack(xs)); y=torch.from_numpy(np.stack(ys))
        optimizer.zero_grad(set_to_none=True)
        _,loss=model(x,y)
        if loss is None or not torch.isfinite(loss): raise FloatingPointError(f"non-finite loss at step {a.start_step+local+1}")
        loss.backward()
        grad=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
        if not torch.isfinite(grad): raise FloatingPointError(f"non-finite gradient at step {a.start_step+local+1}")
        global_step=a.start_step+local+1
        lr=1e-5*min(1.0,global_step/1000)
        for group in optimizer.param_groups: group["lr"]=lr
        optimizer.step(); losses.append(float(loss.detach()))
        if global_step%100==0: print(f"step={global_step} loss={losses[-1]:.5f} source={source}",flush=True)
    end=a.start_step+a.steps; elapsed=time.perf_counter()-started
    loss_tail=(previous_losses+losses)[-1000:]
    checkpoint={"model":model.state_dict(),"model_config":config.__dict__,"step":end,
                "parameter_count":model.parameter_count,"seed":seed,"optimizer_state_dict":optimizer.state_dict(),
                "optimizer_state_included":True,"optimizer":"AdamW","learning_rate":1e-5,
                "corpus_manifest":corpus_info,"loss_tail":loss_tail,
                "training_scope":"real source-scoped RONIN-IA train artifacts only"}
    torch.save(checkpoint,"out/checkpoint.pt")
    progress={"start_step":a.start_step,"end_step":end,"target_steps":TARGET,
              "chunk_steps":a.steps,"training_seconds":elapsed,"initial_loss":losses[0],
              "final_loss":losses[-1],"mean_loss":sum(losses)/len(losses),
              "corpus":corpus_info,"checkpoint_sha256":sha256("out/checkpoint.pt")}
    Path("out/progress.json").write_text(json.dumps(progress,ensure_ascii=False,indent=2)+"\n")
    if end==TARGET:
        after=evaluate(model)
        Path("out/holdout-after.json").write_text(json.dumps(after,ensure_ascii=False,indent=2)+"\n")
        report={"experiment":"HERETIC-500M-real-corpus-250000-steps","start_step":600,"end_step":TARGET,
                "steps_trained":TARGET-600,"parameters":model.parameter_count,"corpus":corpus_info,
                "holdout_before":{k:v for k,v in before.items() if k!="details"},
                "holdout_after":{k:v for k,v in after.items() if k!="details"},
                "accuracy_delta_percentage_points":(after["accuracy"]-before["accuracy"])*100,
                "promotion":"NOT_AUTOMATIC; inspect per-domain results and all 120 predictions"}
        Path("out/final-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(progress,ensure_ascii=False),flush=True)

if __name__=="__main__": main()
