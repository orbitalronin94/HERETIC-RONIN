#!/usr/bin/env python3
"""Continue the distilled 500M student for 10k steps on all admitted local content."""
from __future__ import annotations
import argparse, hashlib, json, re, time
from pathlib import Path
import torch
from ronin.config import ModelConfig
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer
from ronin.data.batches import NextTokenBatches

ROOT=Path("state")
PREFERRED=("domain","skill","difficulty","language","prompt","instruction","question","input","problem","response","answer","completion","output","solution","explanation","reasoning","assumptions","verification","text","content")
IGNORED={"id","uid","domain_id","family_id","scenario_id","split","status","license","source","metadata","tags"}

def sha(path):
 h=hashlib.sha256()
 with Path(path).open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()

def leaves(v):
 if isinstance(v,str): return [v.strip()] if v.strip() else []
 if isinstance(v,list): return [x for y in v for x in leaves(y)]
 if isinstance(v,dict):
  out=[]
  for k in PREFERRED:
   if k in v: out.extend(leaves(v[k]))
  if out: return out
  for k,x in v.items():
   if str(k).lower() not in IGNORED: out.extend(leaves(x))
  return out
 return []

def row_text(row):
 return "\n".join(dict.fromkeys(leaves(row)))

def prepare(args):
 rows=[]; shard_counts={}
 for path in sorted(Path("data/drosophila/parts").glob("*.jsonl")):
  n=0
  for line in path.read_text(encoding="utf-8").splitlines():
   if line.strip():
    obj=json.loads(line)
    if not isinstance(obj,dict): raise ValueError(f"Non-object row: {path}")
    rows.append((path.name,row_text(obj))); n+=1
  shard_counts[path.name]=n
 if len(shard_counts)!=10 or sum(shard_counts.values())!=50000 or any(n!=5000 for n in shard_counts.values()):
  raise RuntimeError(f"Expected 10x5000 Drosophila rows, got {shard_counts}")
 teacher=Path(args.teacher_jsonl)
 teacher_rows=[json.loads(x) for x in teacher.read_text(encoding="utf-8").splitlines() if x.strip()]
 if len(teacher_rows)!=1000: raise RuntimeError(f"Expected 1000 distillation rows, got {len(teacher_rows)}")
 for obj in teacher_rows:
  rows.append(("teacher-multidomain-1000.jsonl",row_text(obj)))
 if any(not text.strip() for _,text in rows): raise RuntimeError("Empty training row")
 corpus="\n\n".join(text for _,text in rows)
 out=Path(args.out); out.mkdir(parents=True,exist_ok=True)
 (out/"corpus.txt").write_text(corpus,encoding="utf-8")
 tokens=torch.tensor(ByteTokenizer().encode(corpus),dtype=torch.long)
 torch.save(tokens,out/"tokens.pt")
 ckpt=torch.load(args.checkpoint,map_location="cpu",weights_only=False)
 if int(ckpt.get("step",-1))!=600 or int(ckpt.get("parameter_count",-1))!=500102144:
  raise RuntimeError("Input is not the exact 500M distilled step-600 checkpoint")
 (out/"student.pt").write_bytes(Path(args.checkpoint).read_bytes())
 manifest={"source_checkpoint_sha256":sha(args.checkpoint),"source_step":600,"parameters":500102144,
  "drosophila_rows":50000,"teacher_distillation_rows":1000,"total_rows":len(rows),
  "drosophila_shards":shard_counts,"corpus_sha256":sha(out/"corpus.txt"),"token_count":int(tokens.numel()),
  "holdout_excluded":True,"scope":"All admitted, versioned training payloads available in this repository at workflow checkout. data/imports contains documentation only; unadmitted source candidates and holdout are excluded."}
 (out/"corpus-manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(manifest,ensure_ascii=False,indent=2),flush=True)

def tasks():
 rows=[]; plurals=[("lápiz","lápices"),("pez","peces"),("luz","luces"),("joven","jóvenes"),("rubí","rubíes"),("régimen","regímenes"),("carácter","caracteres"),("espécimen","especímenes"),("sofá","sofás"),("menú","menús"),("bambú","bambúes"),("crisis","crisis"),("lunes","lunes"),("tórax","tórax"),("análisis","análisis"),("álbum","álbumes"),("examen","exámenes"),("compás","compases"),("raíz","raíces"),("canción","canciones")]
 names=("Alba","Bruno","Celia","Diego","Eva","Fabio","Gala","Hugo")
 for i in range(20):
  a=i+4;b=i%5+2;c=i%4+1; values=[i+1,i+2,i+3]; order=[names[(i+j)%8] for j in range(4)]
  rows += [
   ("mathematics",f"Calcula ({a} + {b}) por {c}, menos {i}. Solo el número.",str((a+b)*c-i)),
   ("programming",f"En Python, ¿qué vale sum({values}) - len({values})? Solo número.",str(sum(values)-len(values))),
   ("logic",f"{order[0]} va antes que {order[1]}, {order[1]} antes que {order[2]} y {order[2]} antes que {order[3]}. ¿Quién va último?",order[3]),
   ("natural_science",f"Una muestra tiene {(i%5+1)*(i+2)} g y ocupa {i%5+1} cm3. ¿Densidad en g/cm3? Solo número.",str(i+2)),
   ("language",f"Escribe el plural de «{plurals[i][0]}». Solo la palabra.",plurals[i][1])]
  amount=i+1
  if i<7: q,a2=f"Convierte {amount} kg a gramos. Solo número.",str(amount*1000)
  elif i<14: q,a2=f"Convierte {amount} litros a mililitros. Solo número.",str(amount*1000)
  else: q,a2=f"Convierte {amount} horas a minutos. Solo número.",str(amount*60)
  rows.append(("interdisciplinary",q,a2))
 return rows

def normalize(v):
 v=v.splitlines()[0] if v.splitlines() else v
 v=v.strip().casefold()
 v=re.sub(r"^(la respuesta es|respuesta:|answer:)","",v).strip()
 return re.sub(r"\s+"," ",v).strip(" \t\r\n.,;:!?¿¡\"'()[]{}")

@torch.inference_mode()
def evaluate(checkpoint,out):
 ck=torch.load(checkpoint,map_location="cpu",weights_only=False)
 cfg=ModelConfig(**ck["model_config"]); model=RoninLM(cfg); model.load_state_dict(ck["model"],strict=True); model.eval()
 tok=ByteTokenizer(); details=[]; counts={}
 for idx,(domain,q,expected) in enumerate(tasks()):
  prompt=tok.encode(f"Q: {q}\nA:"); generated=[]
  for _ in range(32):
   context=(prompt+generated)[-cfg.context_length:]
   logits=model.forward_last_logits(torch.tensor([context],dtype=torch.long),torch.tensor([len(context)-1],dtype=torch.long))
   token=int(torch.argmax(logits[0]).item())
   if token==10: break
   generated.append(token)
  pred=tok.decode(generated).strip(); correct=normalize(pred)==normalize(expected)
  d=counts.setdefault(domain,{"correct":0,"total":0,"blank":0})
  d["correct"]+=int(correct); d["total"]+=1; d["blank"]+=int(not pred)
  details.append({"index":idx,"domain":domain,"question":q,"expected":expected,"prediction":pred,"correct":correct})
 result={"checkpoint":str(checkpoint),"checkpoint_sha256":sha(checkpoint),"step":ck.get("step"),"questions":len(details),
  "correct":sum(x["correct"] for x in details),"accuracy":sum(x["correct"] for x in details)/len(details),
  "blank_predictions":sum(not x["prediction"] for x in details),"by_domain":counts,"predictions":details}
 Path(out).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps({k:v for k,v in result.items() if k!="predictions"},ensure_ascii=False,indent=2),flush=True)

def train(args):
 torch.set_num_threads(4); torch.set_num_interop_threads(1)
 state=Path(args.state); ck=torch.load(state/"student.pt",map_location="cpu",weights_only=False)
 cfg=ModelConfig(**ck["model_config"]); model=RoninLM(cfg); model.load_state_dict(ck["model"],strict=True)
 if model.parameter_count!=500102144: raise RuntimeError("Unexpected student parameter count")
 tokens=torch.load(state/"tokens.pt",map_location="cpu",weights_only=True)
 batches=iter(NextTokenBatches(tokens,1,cfg.context_length,seed=20261106+args.start_step))
 optimizer=torch.optim.AdamW(model.parameters(),lr=1e-5,weight_decay=0.01)
 opt_path=state/"optimizer.pt"
 if opt_path.exists(): optimizer.load_state_dict(torch.load(opt_path,map_location="cpu",weights_only=True))
 losses=[]; model.train(); started=time.perf_counter()
 for i in range(args.steps):
  x,y=next(batches); optimizer.zero_grad(set_to_none=True)
  _,loss=model(x,y)
  if loss is None or not torch.isfinite(loss): raise FloatingPointError(f"Invalid loss at global step {args.start_step+i+1}")
  loss.backward(); norm=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
  if not torch.isfinite(norm): raise FloatingPointError("Non-finite gradient")
  optimizer.step(); losses.append(float(loss.detach()))
  if (i+1)%100==0: print(f"global_step={args.start_step+i+1} loss={losses[-1]:.6f}",flush=True)
 end=args.start_step+args.steps
 out={"model":model.state_dict(),"model_config":cfg.__dict__,"step":end,"parameter_count":model.parameter_count,
      "seed":20261106,"initialization":"continued_from_multidomain_distilled_step_600",
      "corpus_sha256":json.loads((state/"corpus-manifest.json").read_text())["corpus_sha256"],
      "optimizer_state_included":True}
 torch.save(out,state/"student.pt"); torch.save(optimizer.state_dict(),state/"optimizer.pt")
 report={"start_step":args.start_step,"end_step":end,"steps_completed":len(losses),"initial_loss":losses[0],
  "final_loss":losses[-1],"mean_loss":sum(losses)/len(losses),"elapsed_seconds":time.perf_counter()-started,
  "checkpoint_sha256":sha(state/"student.pt"),"optimizer_state_sha256":sha(state/"optimizer.pt")}
 (state/f"stage-{end:05d}.json").write_text(json.dumps(report,indent=2)+"\n")
 print(json.dumps(report,indent=2),flush=True)

p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
a=sub.add_parser("prepare"); a.add_argument("--checkpoint",required=True); a.add_argument("--teacher-jsonl",required=True); a.add_argument("--out",default="state"); a.set_defaults(fn=prepare)
a=sub.add_parser("evaluate"); a.add_argument("--checkpoint",required=True); a.add_argument("--out",required=True); a.set_defaults(fn=lambda x:evaluate(x.checkpoint,x.out))
a=sub.add_parser("train"); a.add_argument("--state",default="state"); a.add_argument("--start-step",type=int,required=True); a.add_argument("--steps",type=int,default=2000); a.set_defaults(fn=train)
args=p.parse_args(); args.fn(args)
