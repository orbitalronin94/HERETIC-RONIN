#!/usr/bin/env python3
"""One optimizer-update benchmark; all variants start from identical weights and micro-batches."""
import argparse,json,os,random,resource,time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import numpy as np
import torch
from ronin.config import ModelConfig
from ronin.models.transformer import RoninLM
from heretic_train_real_corpus_250k import build_corpus
N=40; B=2; C=128
VARIANTS=["baseline","threads-1","threads-2","threads-8","cpu-affinity","mkldnn-disabled","bf16-autocast","torch-compile","adamw-foreach","mmap-batches","sharded-prefetch","packed-window-cache","inference-mode-eval"]
def main():
 p=argparse.ArgumentParser(); p.add_argument("--variant",choices=VARIANTS,required=True); p.add_argument("--create-plan",action="store_true"); p.add_argument("--output",default="out/result.json"); a=p.parse_args(); v=a.variant
 torch.set_num_threads({"threads-1":1,"threads-2":2,"threads-8":8}.get(v,4)); torch.set_num_interop_threads(1)
 affinity=False
 if v=="cpu-affinity" and hasattr(os,"sched_setaffinity"):
  cpus=sorted(os.sched_getaffinity(0))
  if cpus: os.sched_setaffinity(0,set(cpus[:max(1,len(cpus)//2)])); affinity=True
 Path("out").mkdir(parents=True,exist_ok=True)
 ck=torch.load("incoming/checkpoint.pt",map_location="cpu",weights_only=False)
 if int(ck.get("step",-1))!=2600: raise RuntimeError("Expected exact step-2600 checkpoint")
 seed=int(ck.get("seed",20261106))
 torch.manual_seed(seed+2600); np.random.seed((seed+2600)%(2**32-1))
 plan=Path("out/batch-plan.pt")
 if a.create_plan:
  corpus,info=build_corpus(Path("incoming/ronin-ia-train.zip"),Path("incoming/GLOBAL-CORPUS-AUDIT.json"))
 else:
  info=json.load(open("incoming/baseline.json"))["corpus"]
 if a.create_plan:
  rng=random.Random(seed+2600); names=list(corpus); weights=[len(corpus[x])**.5 for x in names]; batches=[]
  for _ in range(N):
   xs=[]; ys=[]
   for _ in range(B):
    name=rng.choices(names,weights=weights,k=1)[0]; buf=corpus[name]; s=rng.randrange(0,len(buf)-C-1); seq=buf[s:s+C+1].astype(np.int64,copy=False); xs.append(seq[:-1]); ys.append(seq[1:])
   batches.append((torch.from_numpy(np.stack(xs)),torch.from_numpy(np.stack(ys))))
  torch.save(batches,plan)
 load0=time.perf_counter()
 batches=torch.load(plan,map_location="cpu",weights_only=False,mmap=(v=="mmap-batches"))
 shard_pool=None
 if v=="sharded-prefetch":
  d=Path("out/shards"); d.mkdir(parents=True,exist_ok=True)
  for i,batch in enumerate(batches): torch.save(batch,d/f"{i:02}.pt")
  shard_files=sorted(d.glob("*.pt"))
  shard_pool=ThreadPoolExecutor(max_workers=2)
  batches=[shard_pool.submit(torch.load,f,weights_only=False) for f in shard_files]
 if v=="packed-window-cache":
  px=torch.stack([x for x,y in batches]); py=torch.stack([y for x,y in batches])
  batches=[(px[i],py[i]) for i in range(len(px))]
 data_prep=time.perf_counter()-load0
 cfg=ModelConfig(**ck["model_config"]); model=RoninLM(cfg); model.load_state_dict(ck["model"],strict=True)
 if model.parameter_count!=500102144: raise RuntimeError(f"Unexpected parameter count {model.parameter_count}")
 if v=="torch-compile": model=torch.compile(model,backend="inductor",fullgraph=False)
 optkw={"foreach":True} if v=="adamw-foreach" else {}
 peak_lr=1e-5*(40**.5)
 opt=torch.optim.AdamW(model.parameters(),lr=peak_lr,betas=(.9,.999),weight_decay=.01,eps=1e-8,**optkw)
 scheduler=torch.optim.lr_scheduler.LambdaLR(opt,lambda step:min(1.0,(step+1)/200))
 lr_used=opt.param_groups[0]["lr"]
 if v=="mkldnn-disabled": torch.backends.mkldnn.enabled=False
 model.train(); opt.zero_grad(set_to_none=True); losses=[]; cpu0=time.process_time(); t0=time.perf_counter()
 for item in batches:
  x,y=item.result() if v=="sharded-prefetch" else item
  with torch.autocast("cpu",dtype=torch.bfloat16,enabled=(v=="bf16-autocast")): _,loss=model(x,y)
  if loss is None or not torch.isfinite(loss): raise FloatingPointError("non-finite loss")
  (loss/N).backward(); losses.append(float(loss.detach().float()))
 grad=torch.nn.utils.clip_grad_norm_(model.parameters(),1.0)
 if not torch.isfinite(grad): raise FloatingPointError("non-finite gradient")
 opt.step(); scheduler.step(); elapsed=time.perf_counter()-t0
 if shard_pool is not None: shard_pool.shutdown(wait=True)
 with torch.no_grad(): fingerprint=float(next(model.parameters()).detach().float().reshape(-1)[:4096].sum())
 out={"variant":v,"status":"completed","checkpoint_step":2600,"optimizer_updates":1,"micro_batches":N,"tokens":N*B*C,"threads":torch.get_num_threads(),"interop_threads":torch.get_num_interop_threads(),"affinity_applied":affinity,"bf16_autocast":v=="bf16-autocast","lr_used":lr_used,"peak_lr":peak_lr,"warmup_optimizer_steps":200,"wall_seconds":elapsed,"data_prep_seconds":data_prep,"end_to_end_seconds":elapsed+data_prep,"cpu_seconds":time.process_time()-cpu0,"tokens_per_second":N*B*C/elapsed,"mean_loss":float(np.mean(losses)),"first_loss":losses[0],"last_loss":losses[-1],"grad_norm":float(grad),"parameter_fingerprint":fingerprint,"peak_rss_mb":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,"corpus":info}
 if v=="inference-mode-eval":
  from heretic_train_real_corpus_250k import evaluate
  t=time.perf_counter()
  with torch.inference_mode(): ev=evaluate(model)
  out["holdout_eval_seconds"]=time.perf_counter()-t; out["holdout_accuracy"]=ev["accuracy"]
 if v=="sharded-prefetch": out["shard_count"]=len(batches); out["prefetch_workers"]=2
 if v=="packed-window-cache": out["packed_shape"]=[len(batches),B,C]
 Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out),flush=True)
if __name__=="__main__": main()
