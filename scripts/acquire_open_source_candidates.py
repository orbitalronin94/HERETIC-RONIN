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
 {"id":"philippesaade/wikidata","config":None,"license":"CC0-1.0","verify_license_tag":True,"limit":5000,"fields":["id","labels","descriptions"],"caveat":"Wikidata structured data is CC0. Keep only labels/descriptions, not linked Wikipedia article text or image assets."},
 {"id":"common-pile/pubmed_filtered","config":None,"license":"per-document CC-BY-4.0 or CC0-1.0 only","license_filter":["creativecommons.org/licenses/by/4.0/","creativecommons.org/publicdomain/zero/1.0/"],"limit":5000,"fields":["text"],"caveat":"Common Pile warns of license metadata errors. Require row-level metadata.license allowlist, preserve article URL/authors/license, and exclude CC-BY-SA, NC, ND and unknown licenses."},
 {"id":"common-pile/stackexchange","config":None,"license":"per-document CC-BY-SA-4.0 only","license_filter":["creativecommons.org/licenses/by-sa/4.0/"],"limit":5000,"fields":["text"],"caveat":"Per-document license required; dataset may contain CC-BY-SA 2.5/3.0 and licensing metadata errors. Only exact 4.0 records are candidates; preserve authors, URL, site and license. Share-alike model implications need separate legal review."},
 {"id":"common-pile/pressbooks_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":5000,"fields":["text"],"caveat":"Open textbook chapters are collected from PressBooks; only exact CC-BY-4.0 records are candidates. Exclude BY-SA, public-domain claims not independently checked, NC, ND and unknown."},
 {"id":"common-pile/libretexts_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":5000,"fields":["text"],"caveat":"Open textbook sections are collected from LibreTexts; only exact CC-BY-4.0 records are candidates. Exclude BY-SA, GFDL, NC, ND and unknown; verify attribution and third-party material."},
 {"id":"secemp9/arxiv-complete","config":"paper_text","license":"per-paper CC-BY-4.0 or CC0-1.0 only","license_filter":["creativecommons.org/licenses/by/4.0/","creativecommons.org/publicdomain/zero/1.0/"],"limit":5000,"fields":["text"],"caveat":"Dataset LICENSE explicitly says compilation CC0 does not relicense papers; paper-level license column governs full text. Only CC-BY-4.0 and CC0 are candidates; exclude arXiv non-exclusive, NULL, NC, ND, BY-SA and other terms. Filter withdrawn stubs, TeX macros/templates and bad renderings."},
 {"id":"common-pile/doab","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":5000,"fields":["text"],"caveat":"DOAB indexes peer-reviewed open-access books and manually whitelists license statements in book front/back matter. Candidate filter accepts exact CC-BY-4.0 only; exclude BY-SA, NC, ND and unknown; check third-party figures."},
 {"id":"common-pile/oercommons_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":5000,"fields":["text"],"caveat":"OERCommons includes public-domain, CC-BY and CC-BY-SA teaching materials; only exact CC-BY-4.0 rows pass. Common Pile warns of possible license metadata errors."},
 {"id":"common-pile/news_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":5000,"fields":["text"],"caveat":"Curated news corpus with per-record license and source URL. Only exact CC-BY-4.0 rows pass; verify publisher/domain rights and attribution; exclude BY-SA, NC, ND and unknown."},
 {"id":"common-pile/cccc","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":5000,"fields":["text"],"caveat":"Creative Commons Common Crawl manually verified top domains and retained domains where CC applies to all text; only exact CC-BY-4.0 per-record licenses pass. Common Pile notes residual license-laundering risk."},
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
  expected_any=set(source.get("verify_license_tags_any",[]))
  license_tag_verified=(expected_tag in tags) if source.get("verify_license_tag") else (bool(expected_any & tags) if expected_any else None)
  if source.get("verify_license_tag") and not license_tag_verified:
   raise RuntimeError(f"{repo}: expected official Hub tag {expected_tag}; found {sorted(tags)}")
  if expected_any and not license_tag_verified:
   raise RuntimeError(f"{repo}: none of required official Hub license tags found: {sorted(expected_any)}; found {sorted(tags)}")
  cfg=source["config"]
  ds=load_dataset(repo,cfg,split="train",streaming=True,revision=revision)
  target=OUT/(repo.replace("/","__")+".jsonl")
  seen=set(); written=0; rejected=0; started=time.time()
  with target.open("w",encoding="utf-8") as f:
   for row in ds:
    row_metadata=row.get("metadata",{}) if isinstance(row.get("metadata",{}),dict) else {}
    row_license=str(row.get("license") or row_metadata.get("license",""))
    allowed=source.get("license_filter",[])
    if allowed and not any(token in row_license.lower() for token in allowed):
     rejected+=1; continue
    chunks=[str(row[k]).strip() for k in source["fields"] if row.get(k)]
    body="\n\n".join(x for x in chunks if x)
    normalized=re.sub(r"\s+"," ",body).strip()
    if len(body)<160 or len(body)>200000 or normalized in seen or EMAIL.search(body) or PHONE.search(body):
     rejected+=1; continue
    seen.add(normalized)
    provenance={k:row[k] for k in ("url","date","language","score","audience","format","seed_data","token_length","id","source","paper_id","title","abstract","primary_category","main_file","resolution","annotation_type","language_code","author","book_url","institution","subject") if k in row}
    for k in ("license","url","authors","site","journal","provenance"):
     if k in row_metadata: provenance["record_"+k]=row_metadata[k]
    record={"text":body,"source":repo,"revision":revision,"config":cfg or "default",
            "license":row_license or source["license"],"source_metadata":provenance}
    f.write(json.dumps(record,ensure_ascii=False)+"\n"); written+=1
    if written>=source["limit"]: break
  if written<source["limit"]//2: raise RuntimeError(f"{repo}: only {written} usable rows")
  manifest.append({"source":repo,"revision":revision,"config":cfg or "default","declared_license":source["license"],"official_license_tag":expected_tag if source.get("verify_license_tag") else None,"official_license_tag_verified":license_tag_verified,
    "rows_written":written,"rows_rejected":rejected,"bytes":target.stat().st_size,"sha256":digest(target),
    "status":"candidate_not_admitted","caveat":source["caveat"],"elapsed_seconds":round(time.time()-started,2),
    "checks":{"streamed_train_only":True,"exact_dedup_within_source":True,"basic_length_filter":True,
      "email_phone_pattern_filter":True,"cross_source_near_duplicate":"PENDING","global_holdout_contamination":"PENDING",
      "human_sample_review":"PENDING","license_review":"per-record allowlist applied; external legal/provenance review pending" if source.get("license_filter") else "source-card-declared; final legal/provenance audit pending","per_record_license_filter":source.get("license_filter",[]),"per_record_license_filter_applied":bool(source.get("license_filter"))}})
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
