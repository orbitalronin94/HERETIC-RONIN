#!/usr/bin/env python3
"""Produce deterministic, stratified-by-source excerpts for human candidate review."""
from __future__ import annotations
import hashlib, json, random, sys
from pathlib import Path

ROOT=Path("staging/open-source-candidates")
OUT=ROOT/"MANUAL-SAMPLE-REVIEW.json"
SEED=20261107
PER_SOURCE=6
MAX_CHARS=700

def main():
    reports=[]
    for path in sorted(ROOT.glob("*.jsonl")):
        rng=random.Random(SEED ^ int(hashlib.sha256(path.name.encode()).hexdigest()[:8],16))
        reservoir=[]; seen=0
        with path.open("r",encoding="utf-8") as stream:
            for line in stream:
                if not line.strip(): continue
                row=json.loads(line); seen+=1
                item={"source":row.get("source"),"revision":row.get("revision"),
                      "config":row.get("config"),"license":row.get("license"),
                      "source_metadata":row.get("source_metadata",{}),
                      "text":str(row.get("text",""))[:MAX_CHARS]}
                if len(reservoir)<PER_SOURCE: reservoir.append(item)
                else:
                    j=rng.randrange(seen)
                    if j<PER_SOURCE: reservoir[j]=item
        if reservoir:
            reports.append({"file":path.name,"rows":seen,"samples":reservoir})
    OUT.write_text(json.dumps({"schema":"heretic-manual-sample-review-v1","seed":SEED,
       "samples_per_source":PER_SOURCE,"sources":reports},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    summary={"schema":"heretic-manual-sample-review-v1","seed":SEED,
       "samples_per_source":PER_SOURCE,
       "sources":[{"file":x["file"],"rows":x["rows"],"sample_count":len(x["samples"])} for x in reports]}
    print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)

if __name__=="__main__": main()
