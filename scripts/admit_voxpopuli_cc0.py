#!/usr/bin/env python3
"""Curate CC0 gold VoxPopuli train transcripts against the complete admitted base corpus."""
from __future__ import annotations
import argparse, gzip, hashlib, json, re, zipfile
from collections import defaultdict
from pathlib import Path
from itertools import combinations
from scripts.audit_heretic_training_corpus import simhash, norm, holdout_rows

SOURCE="facebook/voxpopuli"
REVISION="42f01879c780b4a2e90ec0b4f616c2ece526e4f1"
CONFIGS={"es","en","de","fr","it","pl"}
MIN_CHARS=40

def base_texts(z):
    out=[]
    def add(stream):
        for line in stream:
            if line.strip():
                row=json.loads(line); t=row.get("text","")
                if isinstance(t,str) and len(t.strip())>=MIN_CHARS: out.append(t)
    manifest=json.loads(z.read("IMPORT-MANIFEST.json"))
    if manifest.get("records_staged")!=286464 or manifest.get("active_training_authorized") is not False:
        raise RuntimeError("Unexpected RONIN-IA import manifest; fail closed")
    with z.open("covost2-cc0/train.jsonl.gz") as raw, gzip.GzipFile(fileobj=raw) as f: add(f)
    with z.open("mathlib4-apache/documents.train.jsonl.gz") as raw, gzip.GzipFile(fileobj=raw) as f: add(f)
    with z.open("scienceverse-ccby/documents.train.jsonl") as f: add(f)
    for name in z.namelist():
        if name.startswith("ronin-authored-papers/") and name.endswith(".md"):
            t=z.read(name).decode("utf-8")
            if len(t.strip())>=MIN_CHARS: out.append(t)
    for name in ("literature-es/train.txt","nasa-ntrs-file-reviewed/train.txt"):
        t=z.read(name).decode("utf-8")
        if name.startswith("literature"):
            out.extend(p for p in t.split("\n\n") if len(p.strip())>=MIN_CHARS)
        elif len(t.strip())>=MIN_CHARS: out.append(t)
    return out

def bands(h):
    return [(i,(h>>(i*16))&0xffff) for i in range(4)]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--base-zip",type=Path,required=True)
    p.add_argument("--candidate-zip",type=Path,required=True)
    p.add_argument("--out",type=Path,default=Path("staging/admitted/voxpopuli-cc0"))
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    docs=[]
    with zipfile.ZipFile(a.base_zip) as z: docs=base_texts(z)
    exact=set(); buckets=defaultdict(list); hashes=[]
    for idx,t in enumerate(docs):
        n=norm(t)
        if not n: continue
        exact.add(hashlib.sha256(n.encode()).hexdigest())
        h=simhash(t); hashes.append(h)
        for key in bands(h): buckets[key].append(h)
    holdout=[norm(x["question"]) for x in holdout_rows()]
    counts={}; accepted=0; rejected={"license_or_provenance":0,"invalid_text":0,"duplicate_exact":0,"duplicate_near":0,"holdout_match":0,"not_gold":0}
    seen_candidate=set(); out_path=a.out/"voxpopuli-cc0-train.jsonl"
    manifest_sources=[]
    with zipfile.ZipFile(a.candidate_zip) as z, out_path.open("w",encoding="utf-8") as out:
        names=[n for n in z.namelist() if re.search(r"facebook__voxpopuli__(es|en|de|fr|it|pl)__train\.jsonl$",n)]
        if len(names)!=6: raise RuntimeError(f"Expected six VoxPopuli language shards; found {len(names)}")
        for name in sorted(names):
            config=re.search(r"voxpopuli__(\w+)__",name).group(1)
            rows=0; kept=0
            with z.open(name) as f:
                for raw in f:
                    if not raw.strip(): continue
                    row=json.loads(raw); rows+=1
                    if row.get("source")!=SOURCE or row.get("revision")!=REVISION or row.get("config")!=config or row.get("license")!="CC0-1.0":
                        rejected["license_or_provenance"]+=1; continue
                    meta=row.get("source_metadata") or {}
                    if meta.get("is_gold_transcript") is not True:
                        rejected["not_gold"]+=1; continue
                    t=row.get("text")
                    if not isinstance(t,str) or len(t.strip())<MIN_CHARS or len(t)>100000:
                        rejected["invalid_text"]+=1; continue
                    n=norm(t); digest=hashlib.sha256(n.encode()).hexdigest()
                    if digest in exact or digest in seen_candidate:
                        rejected["duplicate_exact"]+=1; continue
                    if any(len(q)>=24 and q in n for q in holdout):
                        rejected["holdout_match"]+=1; continue
                    h=simhash(t); possible=set()
                    for key in bands(h): possible.update(buckets.get(key,[]))
                    if any((h^other).bit_count()<=3 for other in possible):
                        rejected["duplicate_near"]+=1; continue
                    seen_candidate.add(digest)
                    for key in bands(h): buckets[key].append(h)
                    exact.add(digest)
                    out.write(json.dumps({"text":t,"source":SOURCE,"revision":REVISION,"config":config,"language":config,"license":"CC0-1.0","attribution":"VoxPopuli; European Parliament; CC0-1.0"},ensure_ascii=False)+"\n")
                    kept+=1; accepted+=1
            counts[config]={"candidate_rows":rows,"admitted_rows":kept}
            manifest_sources.append({"file":name,"revision":REVISION,"config":config,"license":"CC0-1.0"})
    size=out_path.stat().st_size
    digest=hashlib.sha256(out_path.read_bytes()).hexdigest()
    report={"schema":"heretic-admitted-dataset-v1","source":SOURCE,"source_revision":REVISION,"split":"train","configs":sorted(CONFIGS),"license":"CC0-1.0","rows_candidate":sum(x["candidate_rows"] for x in counts.values()),"rows_admitted":accepted,"bytes_admitted":size,"sha256":digest,"language_counts":counts,"rejections":rejected,"source_shards":manifest_sources,"deduplication":"Exact SHA-256 over normalized text plus 64-bit word-trigram SimHash, Hamming <=3, against the complete admitted RONIN-IA base corpus and earlier accepted VoxPopuli rows.","holdout":"120-question exact-match diagnostic; no exact matches admitted.","training_authorized":accepted>0,"scope":"Gold transcript text only; train split; no audio, speaker IDs, gender, demographics or validation/test data."}
    (a.out/"ADMISSION-MANIFEST.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if accepted==0: raise SystemExit("No VoxPopuli rows passed admission gates")
if __name__=="__main__": main()
