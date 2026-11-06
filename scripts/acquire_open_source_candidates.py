#!/usr/bin/env python3
"""Acquire bounded, pinned open-source corpus slices as unadmitted candidates."""
from __future__ import annotations
import hashlib, json, os, re, sys, time
from pathlib import Path
from datasets import load_dataset
from huggingface_hub import HfApi

OUT=Path("staging/open-source-candidates")
SOURCES=[
 {"id":"HuggingFaceFW/fineweb-edu","config":"sample-10BT","license":"ODC-By-1.0","limit":5000,"fields":["text"],"caveat":"Common Crawl source-page rights and terms remain applicable."},
 {"id":"open-web-math/open-web-math","config":None,"license":"ODC-By-1.0","limit":5000,"fields":["text"],"caveat":"Common Crawl terms apply; collection license does not relicense underlying pages."},
 {"id":"HuggingFaceTB/cosmopedia","config":"auto_math_text","license":"Apache-2.0","limit":5000,"fields":["text","prompt"],"caveat":"Verify per-config card and source lineage; synthetic quality requires audit."},
 {"id":"HuggingFaceTB/smollm-corpus","config":"cosmopedia-v2","license":"ODC-By-1.0","limit":5000,"fields":["text","prompt"],"caveat":"Synthetic data seeded from web/educational sources; quality and source-derived risks require audit."},
 {"id":"CohereLabs/aya_dataset","config":"default","license":"Apache-2.0","verify_license_tag":True,"limit":5000,"fields":["inputs","targets"],"caveat":"Official card states Apache-2.0 for any purpose. Human annotations and re-annotations; default config only. Do not load demographics config or user_id. Retain language and annotation_type; inspect PII and upstream prompt lineage."},
]
EMAIL=re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
PHONE=re.compile(r"(?<!\d)(?:\+?\d[\d .()/-]{7,}\d)(?!\d)")
def digest(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True); api=HfApi(); manifest=[]
 for source in SOURCES:
  repo=source["id"]; info=api.dataset_info(repo); revision=info.sha
  tags=set(info.tags or [])
  expected_tag="license:"+source["license"].lower()
  license_tag_verified=expected_tag in tags
  if source.get("verify_license_tag") and not license_tag_verified:
   raise RuntimeError(f"{repo}: expected official Hub tag {expected_tag}; found {sorted(tags)}")
  cfg=source["config"]
  ds=load_dataset(repo,cfg,split="train",streaming=True,revision=revision)
  target=OUT/(repo.replace("/","__")+".jsonl")
  seen=set(); written=0; rejected=0; started=time.time()
  with target.open("w",encoding="utf-8") as f:
   for row in ds:
    chunks=[str(row[k]).strip() for k in source["fields"] if row.get(k)]
    body="\n\n".join(x for x in chunks if x)
    normalized=re.sub(r"\s+"," ",body).strip()
    if len(body)<160 or len(body)>200000 or normalized in seen or EMAIL.search(body) or PHONE.search(body):
     rejected+=1; continue
    seen.add(normalized)
    record={"text":body,"source":repo,"revision":revision,"config":cfg or "default",
            "license":source["license"],"source_metadata":{k:row[k] for k in ("url","date","language","score","audience","format","seed_data","token_length") if k in row}}
    f.write(json.dumps(record,ensure_ascii=False)+"\n"); written+=1
    if written>=source["limit"]: break
  if written<source["limit"]//2: raise RuntimeError(f"{repo}: only {written} usable rows")
  manifest.append({"source":repo,"revision":revision,"config":cfg or "default","declared_license":source["license"],"official_license_tag":expected_tag if source.get("verify_license_tag") else None,"official_license_tag_verified":license_tag_verified,
    "rows_written":written,"rows_rejected":rejected,"bytes":target.stat().st_size,"sha256":digest(target),
    "status":"candidate_not_admitted","caveat":source["caveat"],"elapsed_seconds":round(time.time()-started,2),
    "checks":{"streamed_train_only":True,"exact_dedup_within_source":True,"basic_length_filter":True,
      "email_phone_pattern_filter":True,"cross_source_near_duplicate":"PENDING","global_holdout_contamination":"PENDING",
      "human_sample_review":"PENDING","license_review":"source-card-declared; final legal/provenance audit pending"}})
  print(json.dumps(manifest[-1],ensure_ascii=False),flush=True)
 result={"schema":"heretic-open-source-candidate-bundle-v1","status":"candidate_not_admitted","training_authorized":False,
  "policy":"No candidate may train until cross-source deduplication, holdout contamination, human sample review and per-source license/provenance gates pass.",
  "sources":manifest,"total_rows":sum(x["rows_written"] for x in manifest),
  "total_bytes":sum(x["bytes"] for x in manifest)}
 (OUT/"OPEN-SOURCE-MANIFEST.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
 # PyArrow may abort during interpreter teardown on hosted runners; all outputs are closed and flushed.
 sys.stdout.flush(); sys.stderr.flush(); os._exit(0)
if __name__=="__main__": main()
