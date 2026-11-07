#!/usr/bin/env python3
"""Acquire bounded, pinned open-source corpus slices as unadmitted candidates."""
from __future__ import annotations
import hashlib, json, os, re, sys, time
from itertools import chain
from pathlib import Path
from datasets import load_dataset
from huggingface_hub import HfApi

OUT=Path("staging/open-source-candidates")
TARGET_BYTES=6_800_000_000  # 10x the currently effective 680,665,972-byte corpus
SOURCES=[
 {"id":"HuggingFaceFW/fineweb-edu","config":"sample-10BT","license":"ODC-By-1.0","limit":100000,"fields":["text"],"caveat":"Common Crawl source-page rights and terms remain applicable."},
 {"id":"open-web-math/open-web-math","config":None,"license":"ODC-By-1.0","limit":100000,"fields":["text"],"caveat":"Common Crawl terms apply; collection license does not relicense underlying pages."},
 {"id":"HuggingFaceTB/cosmopedia","config":"auto_math_text","license":"Apache-2.0","limit":50000,"fields":["text","prompt"],"caveat":"Verify per-config card and source lineage; synthetic quality requires audit."},
 {"id":"HuggingFaceTB/smollm-corpus","config":"cosmopedia-v2","license":"ODC-By-1.0","limit":50000,"fields":["text","prompt"],"caveat":"Synthetic data seeded from web/educational sources; quality and source-derived risks require audit."},
 {"id":"CohereLabs/aya_dataset","config":"default","license":"Apache-2.0","verify_license_tag":True,"limit":25000,"fields":["inputs","targets"],"caveat":"Official card states Apache-2.0 for any purpose. Human annotations and re-annotations; default config only. Do not load demographics config or user_id. Retain language and annotation_type; inspect PII and upstream prompt lineage."},
 {"id":"philippesaade/wikidata","config":None,"license":"CC0-1.0","verify_license_tag":True,"limit":50000,"fields":["id","labels","descriptions"],"caveat":"Wikidata structured data is CC0. Keep only labels/descriptions, not linked Wikipedia article text or image assets."},
 {"id":"common-pile/pubmed_filtered","optional":True,"config":None,"license":"per-document CC-BY-4.0 or CC0-1.0 only","license_filter":["creativecommons.org/licenses/by/4.0/","creativecommons.org/publicdomain/zero/1.0/"],"limit":50000,"fields":["text"],"caveat":"Common Pile warns of license metadata errors. Require row-level metadata.license allowlist, preserve article URL/authors/license, and exclude CC-BY-SA, NC, ND and unknown licenses."},
 {"id":"common-pile/stackexchange","config":None,"license":"per-document CC-BY-SA-4.0 only","license_filter":["creativecommons.org/licenses/by-sa/4.0/"],"limit":50000,"fields":["text"],"caveat":"Per-document license required; dataset may contain CC-BY-SA 2.5/3.0 and licensing metadata errors. Only exact 4.0 records are candidates; preserve authors, URL, site and license. Share-alike model implications need separate legal review."},
 {"id":"common-pile/pressbooks_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":50000,"fields":["text"],"caveat":"Open textbook chapters are collected from PressBooks; only exact CC-BY-4.0 records are candidates. Exclude BY-SA, public-domain claims not independently checked, NC, ND and unknown."},
 {"id":"common-pile/libretexts_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":50000,"fields":["text"],"caveat":"Open textbook sections are collected from LibreTexts; only exact CC-BY-4.0 records are candidates. Exclude BY-SA, GFDL, NC, ND and unknown; verify attribution and third-party material."},
 {"id":"secemp9/arxiv-complete","config":"paper_text","license":"per-paper CC-BY-4.0 or CC0-1.0 only","license_filter":["creativecommons.org/licenses/by/4.0/","creativecommons.org/publicdomain/zero/1.0/"],"limit":100000,"fields":["text"],"caveat":"Dataset LICENSE explicitly says compilation CC0 does not relicense papers; paper-level license column governs full text. Only CC-BY-4.0 and CC0 are candidates; exclude arXiv non-exclusive, NULL, NC, ND, BY-SA and other terms. Filter withdrawn stubs, TeX macros/templates and bad renderings."},
 {"id":"common-pile/doab","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":50000,"fields":["text"],"caveat":"DOAB indexes peer-reviewed open-access books and manually whitelists license statements in book front/back matter. Candidate filter accepts exact CC-BY-4.0 only; exclude BY-SA, NC, ND and unknown; check third-party figures."},
 {"id":"common-pile/oercommons_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":10000,"min_rows":100,"fields":["text"],"caveat":"OERCommons includes public-domain, CC-BY and CC-BY-SA teaching materials; only exact CC-BY-4.0 rows pass. Common Pile warns of possible license metadata errors."},
 {"id":"common-pile/news_filtered","config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":10000,"fields":["text"],"caveat":"Curated news corpus with per-record license and source URL. Only exact CC-BY-4.0 rows pass; verify publisher/domain rights and attribution; exclude BY-SA, NC, ND and unknown."},
 {"id":"openslr/librispeech_asr","config":"all","split":"train.clean.100","license":"CC-BY-4.0","verify_license_tag":True,"limit":50000,"fields":["text"],"caveat":"Transcript text only; do not ingest audio, speaker_id, chapter_id or validation/test splits. Attribute Panayotov et al. and OpenSLR."},
 {"id":"openslr/librispeech_asr","config":"all","split":"train.clean.360","license":"CC-BY-4.0","verify_license_tag":True,"limit":50000,"fields":["text"],"caveat":"Transcript text only; do not ingest audio, speaker_id, chapter_id or validation/test splits. Attribute Panayotov et al. and OpenSLR."},
 {"id":"facebook/voxpopuli","config":"es","split":"train","license":"CC0-1.0","verify_license_tag":True,"limit":20000,"fields":["normalized_text"],"required_true_fields":["is_gold_transcript"],"metadata_fields":["language"],"caveat":"Gold transcript text only; exclude audio, speaker_id, gender and all validation/test data. VoxPopuli data is CC0; retain European Parliament provenance and corpus citation."},
 {"id":"facebook/voxpopuli","config":"en","split":"train","license":"CC0-1.0","verify_license_tag":True,"limit":20000,"fields":["normalized_text"],"required_true_fields":["is_gold_transcript"],"metadata_fields":["language"],"caveat":"Gold transcript text only; exclude audio, speaker_id, gender and all validation/test data. VoxPopuli data is CC0; retain European Parliament provenance and corpus citation."},
 {"id":"facebook/voxpopuli","config":"de","split":"train","license":"CC0-1.0","verify_license_tag":True,"limit":20000,"fields":["normalized_text"],"required_true_fields":["is_gold_transcript"],"metadata_fields":["language"],"caveat":"Gold transcript text only; exclude audio, speaker_id, gender and all validation/test data. VoxPopuli data is CC0; retain European Parliament provenance and corpus citation."},
 {"id":"facebook/voxpopuli","config":"fr","split":"train","license":"CC0-1.0","verify_license_tag":True,"limit":20000,"fields":["normalized_text"],"required_true_fields":["is_gold_transcript"],"metadata_fields":["language"],"caveat":"Gold transcript text only; exclude audio, speaker_id, gender and all validation/test data. VoxPopuli data is CC0; retain European Parliament provenance and corpus citation."},
 {"id":"facebook/voxpopuli","config":"it","split":"train","license":"CC0-1.0","verify_license_tag":True,"limit":20000,"fields":["normalized_text"],"required_true_fields":["is_gold_transcript"],"metadata_fields":["language"],"caveat":"Gold transcript text only; exclude audio, speaker_id, gender and all validation/test data. VoxPopuli data is CC0; retain European Parliament provenance and corpus citation."},
 {"id":"facebook/voxpopuli","config":"pl","split":"train","license":"CC0-1.0","verify_license_tag":True,"limit":20000,"fields":["normalized_text"],"required_true_fields":["is_gold_transcript"],"metadata_fields":["language"],"caveat":"Gold transcript text only; exclude audio, speaker_id, gender and all validation/test data. VoxPopuli data is CC0; retain European Parliament provenance and corpus citation."},
 {"id":"common-pile/cccc","optional":True,"config":None,"license":"per-document CC-BY-4.0 only","license_filter":["creativecommons.org/licenses/by/4.0/"],"limit":150000,"fields":["text"],"caveat":"Common Pile manually verified domain-level CC claims but documents residual licensing errors. Exact per-record CC-BY-4.0 URI only; preserve URL/domain/date/license and audit opt-outs, PII, quality and cross-corpus duplication."},
 {"id":"common-pile/data_provenance_initiative_filtered","config":None,"license":"per-document MIT/Apache/BSD/CC-BY-4.0/CC0 only","license_name_filter":["mit license","apache license 2.0","apache-2.0","bsd 2-clause license","bsd 3-clause license","bsd-2-clause","bsd-3-clause","creative commons attribution 4.0 international","cc-by-4.0","cc0 1.0 universal","cc0-1.0"],"limit":50000,"fields":["text"],"caveat":"DPI manually annotates per-document provenance/license but warns of license laundering and metadata errors. Exact allowlist only; preserve metadata.license, license_url and dataset_id; candidate only pending independent rights and quality review."},
 {"id":"common-pile/pubmed_filtered","config":None,"license":"per-document CC-BY-4.0 or CC0-1.0 only","license_filter":["creativecommons.org/licenses/by/4.0/","creativecommons.org/publicdomain/zero/1.0/"],"limit":20000,"min_rows":1000,"fields":["text"],"caveat":"Large PMC OA corpus. Only exact CC-BY-4.0 or CC0 per-record metadata. Dataset paper warns of license metadata errors; retain article URL/authors/license and keep candidate-only until manual rights/provenance review."},
 {"id":"open-thoughts/OpenThoughts3-1.2M","config":None,"license":"Apache-2.0","verify_license_tag":True,"limit":15000,"min_rows":1000,"fields":["conversations"],"caveat":"Official card declares Apache-2.0; 1.2M math/code/science rows. Questions include upstream StackExchange and NVIDIA/OpenCodeReasoning sources; Apache dataset tag does not automatically clear third-party prompt rights. Candidate only pending source-level lineage review."},
 {"id":"open-r1/OpenR1-Math-220k","config":"default","license":"Apache-2.0","verify_license_tag":True,"limit":12000,"min_rows":1000,"fields":["problem","solution","answer"],"caveat":"Official card declares Apache-2.0. Solutions are generated from NuminaMath 1.5 problems; inspect upstream rights and per-row source metadata before admission. Only default train config; candidate only."},
 {"id":"IFM/Code-Reasoning","config":"code-no-thinking","license":"Apache-2.0","verify_license_tag":True,"limit":12000,"min_rows":1000,"fields":["text"],"caveat":"Official card declares Apache-2.0 and train-only text; source lineage and generated-content provenance are not fully enumerated. Candidate only pending manual sample and rights review."},
 {"id":"IFM/Math-Reasoning","config":"math-dialogue","license":"Apache-2.0","verify_license_tag":True,"limit":12000,"min_rows":1000,"fields":["text"],"caveat":"Official card declares Apache-2.0 and train-only text; inspect dialogue quality, correctness and upstream/generated-data provenance. Candidate only pending manual review."},
 {"id":"docketx/us-caselaw-fed-district","config":"default","license":"CC0-1.0","verify_license_tag":True,"limit":100000,"min_rows":1000,"fields":["text"],"metadata_fields":["id","jurisdiction","title","source","license","citation","court","date"],"caveat":"1.3M-row district-court opinion slice from Free Law Project/CourtListener bulk export. Dataset card identifies U.S. judicial opinions as public-domain government edicts and the packaging as CC0. Preserve citation/court/date; exclude non-opinion additions; legal text is domain-specific and not a substitute for legal advice."},
 {"id":"crumb/openstax-text","config":None,"license":"CC-BY-4.0","verify_license_tag":True,"limit":50000,"min_rows":1000,"fields":["text"],"caveat":"3.35M text rows from 76 OpenStax textbooks. Dataset card is CC-BY-4.0 and embedded textbook pages carry attribution, but OpenStax licensing varies by title/edition; verify each book-level license and retain attribution before admission. Candidate only."},
 {"id":"PleIAs/Spanish-PD-Books","config":None,"data_files":["spanish_pd_1.parquet","spanish_pd_10.parquet","spanish_pd_100.parquet","spanish_pd_101.parquet"],"license":"EU public domain claimed by publisher (author death >70 years)","limit":12000,"min_rows":1000,"fields":["text"],"metadata_fields":["identifier","creator","title","publication_date","word_count"],"caveat":"52.1GB collection / 302,640 Spanish texts / 13.9B words, aggregated from BDH and Internet Archive. This acquisition reads only four pinned parquet shards; preserve creator/title/publication metadata. Dataset card asserts EU public domain based on author death >70 years, but each sampled work needs independent metadata/rights review and OCR quality review. Candidate only; no blanket admission."},
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
  try:
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
   split=source.get("split","train")
   if source.get("data_files"):
    remote_files=[f"hf://datasets/{repo}@{revision}/{name}" for name in source["data_files"]]
    ds=load_dataset("parquet",data_files={"train":remote_files},split=split,streaming=True)
   else:
    ds=load_dataset(repo,cfg,split=split,streaming=True,revision=revision)
   available_columns=set(ds.features.keys()) if ds.features is not None else set(ds.column_names or [])
   # Some JSON/JSON.GZ streaming datasets expose neither Features nor column_names.
   # Infer their schema from the first actual row and chain it back into the stream.
   if not available_columns:
    iterator=iter(ds)
    try:
     first_row=next(iterator)
    except StopIteration:
     raise RuntimeError(f"{repo}/{cfg or 'default'}: empty train split")
    if not isinstance(first_row,dict):
     raise RuntimeError(f"{repo}/{cfg or 'default'}: first streamed row is not an object")
    available_columns=set(first_row.keys())
    ds=chain((first_row,),iterator)
   required_columns=list(dict.fromkeys(source["fields"]+source.get("required_true_fields",[])+source.get("metadata_fields",[])))
   missing_columns=[column for column in required_columns if column not in available_columns]
   if missing_columns:
    message=f"{repo}/{cfg or 'default'}: missing required columns {missing_columns}; available={sorted(available_columns)}"
    if source.get("optional"):
     manifest.append({"source":repo,"revision":revision,"config":cfg or "default","selected_files":source.get("data_files",[]),"split":split,"declared_license":source["license"],"rows_written":0,"rows_rejected":0,"bytes":0,"sha256":None,"status":"skipped_schema_mismatch","caveat":message,"checks":{"streamed_train_only":True,"cross_source_near_duplicate":"NOT_RUN","global_holdout_contamination":"NOT_RUN","human_sample_review":"NOT_RUN"}})
     print(json.dumps(manifest[-1],ensure_ascii=False),flush=True)
     continue
    raise RuntimeError(message)
   # Keep per-record rights metadata when a source requires license filtering.
   # The payload projection still excludes all unrequested columns (notably audio).
   optional_rights_columns=[column for column in ("metadata","license") if column in available_columns and (source.get("license_filter") or source.get("license_name_filter"))]
   selected_columns=list(dict.fromkeys(required_columns+optional_rights_columns))
   if hasattr(ds,"select_columns") and getattr(ds,"features",None) is not None:
    ds=ds.select_columns(selected_columns)
   safe_config=(cfg or "default").replace("/","__")
   safe_split=split.replace("/","__").replace(".","_")
   target=OUT/(repo.replace("/","__")+"__"+safe_config+"__"+safe_split+".jsonl")
   seen=set(); written=0; rejected=0; started=time.time()
   with target.open("w",encoding="utf-8") as f:
    for row in ds:
     if any(row.get(k) is not True for k in source.get("required_true_fields",[])):
      rejected+=1; continue
     row_metadata=row.get("metadata",{}) if isinstance(row.get("metadata",{}),dict) else {}
     raw_license=row.get("license") or row_metadata.get("license","")
     license_values=raw_license if isinstance(raw_license,list) else [raw_license]
     row_license="; ".join(str(x).strip() for x in license_values if x is not None)
     allowed=source.get("license_filter",[])
     name_allowed=source.get("license_name_filter",[])
     license_text=row_license.lower()
     if allowed and not any(token in license_text for token in allowed):
      rejected+=1; continue
     if name_allowed and not any(token in license_text for token in name_allowed):
      rejected+=1; continue
     if (allowed or name_allowed) and not row_license:
      rejected+=1; continue
     def render_value(value):
      if isinstance(value,str): return value.strip()
      if isinstance(value,list):
       rendered=[]
       for item in value:
        if isinstance(item,dict):
         role=item.get("from",item.get("role",""))
         content=item.get("value",item.get("content",""))
         if content: rendered.append((str(role)+": " if role else "")+str(content))
        elif item is not None: rendered.append(str(item))
       return "\n\n".join(rendered)
      if isinstance(value,dict): return json.dumps(value,ensure_ascii=False,sort_keys=True)
      return str(value).strip() if value is not None else ""
     chunks=[render_value(row.get(k)) for k in source["fields"]]
     body="\n\n".join(x for x in chunks if x)
     normalized=re.sub(r"\s+"," ",body).strip()
     if len(body)<160 or len(body)>200000 or normalized in seen or EMAIL.search(body) or PHONE.search(body):
      rejected+=1; continue
     seen.add(normalized)
     provenance={k:row[k] for k in ("url","date","language","score","audience","format","seed_data","token_length","id","source","paper_id","title","abstract","primary_category","main_file","resolution","annotation_type","language_code","author","book_url","institution","subject","is_gold_transcript","creator","publication_date","word_count","identifier","jurisdiction","citation","court","date","domain","difficulty","problem_type","question_type","token_count") if k in row}
     for k in ("license","url","authors","author","site","journal","provenance","license_url","dataset_id","language","annotation_type","book_url","title","institution","subject","creator","publication_date","word_count","identifier","jurisdiction","citation","court","date"):
      if k in row_metadata: provenance["record_"+k]=row_metadata[k]
     record={"text":body,"source":repo,"revision":revision,"config":cfg or "default","selected_files":source.get("data_files",[]),
             "license":row_license or source["license"],"source_metadata":provenance}
     f.write(json.dumps(record,ensure_ascii=False)+"\n"); written+=1
     if written>=source["limit"]: break
   if written<source.get("min_rows",source["limit"]//2): raise RuntimeError(f"{repo}: only {written} usable rows")
   manifest.append({"source":repo,"revision":revision,"config":cfg or "default","split":split,"declared_license":source["license"],"official_license_tag":expected_tag if source.get("verify_license_tag") else None,"official_license_tag_verified":license_tag_verified,
     "rows_written":written,"rows_rejected":rejected,"bytes":target.stat().st_size,"sha256":digest(target),
     "status":"candidate_not_admitted","caveat":source["caveat"],"elapsed_seconds":round(time.time()-started,2),
     "checks":{"streamed_train_only":True,"exact_dedup_within_source":True,"basic_length_filter":True,
       "email_phone_pattern_filter":True,"required_true_fields":source.get("required_true_fields",[]),"selected_columns":selected_columns,"cross_source_near_duplicate":"PENDING","global_holdout_contamination":"PENDING",
       "human_sample_review":"PENDING","license_review":"per-record allowlist applied; external legal/provenance review pending" if source.get("license_filter") else "source-card-declared; final legal/provenance audit pending","per_record_license_filter":source.get("license_filter",[]),"per_record_license_filter_applied":bool(source.get("license_filter"))}})
   print(json.dumps(manifest[-1],ensure_ascii=False),flush=True)

  except Exception as exc:
   failure={"source":source.get("id","unknown"),"revision":None,"config":source.get("config") or "default","split":source.get("split","train"),"declared_license":source.get("license"),"rows_written":0,"rows_rejected":0,"bytes":0,"sha256":None,"status":"source_failed_nonfatal","caveat":f"{type(exc).__name__}: {exc}","checks":{"cross_source_near_duplicate":"NOT_RUN","global_holdout_contamination":"NOT_RUN","human_sample_review":"NOT_RUN"}}
   manifest.append(failure)
   print(json.dumps(failure,ensure_ascii=False),flush=True)
 result={"schema":"heretic-open-source-candidate-bundle-v1","status":"candidate_not_admitted","training_authorized":False,
  "policy":"No candidate may train until cross-source deduplication, holdout contamination, human sample review and per-source license/provenance gates pass.",
  "sources":manifest,"total_rows":sum(x["rows_written"] for x in manifest),
  "total_bytes":sum(x["bytes"] for x in manifest),
  "target_bytes":TARGET_BYTES,"target_met":sum(x["bytes"] for x in manifest)>=TARGET_BYTES,
  "scale_factor_vs_current_effective_corpus":sum(x["bytes"] for x in manifest)/680665972,
  "source_failures":[x["source"] for x in manifest if x["status"]=="source_failed_nonfatal"],
  "policy":"Candidate bytes do not become effective training bytes until global deduplication, holdout contamination, source rights and quality gates pass."}
 (OUT/"OPEN-SOURCE-MANIFEST.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
 print(json.dumps(result,ensure_ascii=False,indent=2),flush=True)
 # PyArrow may abort during interpreter teardown on hosted runners; all outputs are closed and flushed.
 sys.stdout.flush(); sys.stderr.flush(); os._exit(0)
if __name__=="__main__": main()
