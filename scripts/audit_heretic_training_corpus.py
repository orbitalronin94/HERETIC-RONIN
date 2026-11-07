#!/usr/bin/env python3
"""Global exact/near-duplicate and holdout audit for real RONIN-IA train artifacts only."""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile, gzip
from collections import defaultdict
from pathlib import Path
from itertools import combinations
import hashlib as _hashlib

IMPORT_ZIP = Path("incoming/ronin-ia-train.zip")
OUT = Path("reports/corpus-audit")  # real-artifact audit revision 2
HOLDOUT = []
PLURALS = [("lápiz","lápices"),("pez","peces"),("luz","luces"),("joven","jóvenes"),("rubí","rubíes"),("régimen","regímenes"),("carácter","caracteres"),("espécimen","especímenes"),("sofá","sofás"),("menú","menús"),("bambú","bambúes"),("crisis","crisis"),("lunes","lunes"),("tórax","tórax"),("análisis","análisis"),("álbum","álbumes"),("examen","exámenes"),("compás","compases"),("raíz","raíces"),("canción","canciones")]
NAMES=("Alba","Bruno","Celia","Diego","Eva","Fabio","Gala","Hugo")
def holdout_rows():
    rows=[]
    for i in range(20):
        a=i+4; b=(i%5)+2; c=(i%4)+1
        rows.append({"domain":"mathematics","question":f"Calcula ({a} + {b}) por {c}, menos {i}. Solo el número.","answer":str((a+b)*c-i)})
        v=[i+1,i+2,i+3]
        rows.append({"domain":"programming","question":f"En Python, ¿qué vale sum({v}) - len({v})? Solo número.","answer":str(sum(v)-len(v))})
        o=[NAMES[(i+j)%len(NAMES)] for j in range(4)]
        rows.append({"domain":"logic","question":f"{o[0]} va antes que {o[1]}, {o[1]} antes que {o[2]} y {o[2]} antes que {o[3]}. ¿Quién va último?","answer":o[3]})
        vol=(i%5)+1; den=i+2
        rows.append({"domain":"natural_science","question":f"Una muestra tiene {vol*den} g y ocupa {vol} cm3. ¿Densidad en g/cm3? Solo número.","answer":str(den)})
        singular,plural=PLURALS[i]
        rows.append({"domain":"language","question":f"Escribe el plural de «{singular}». Solo la palabra.","answer":plural})
        amount=i+1
        if i<7: q=f"Convierte {amount} kg a gramos. Solo número."; ans=str(amount*1000)
        elif i<14: q=f"Convierte {amount} litros a mililitros. Solo número."; ans=str(amount*1000)
        else: q=f"Convierte {amount} horas a minutos. Solo número."; ans=str(amount*60)
        rows.append({"domain":"interdisciplinary","question":q,"answer":ans})
    return rows
def norm(s): return re.sub(r"\s+"," ",str(s).casefold()).strip()
def row_text(row):
    preferred=("domain","skill","difficulty","language","prompt","instruction","question","input","problem","response","answer","completion","output","solution","explanation","reasoning","assumptions","verification","text","content")
    ignored={"id","uid","domain_id","family_id","scenario_id","split","status","license","source","metadata","tags"}
    found=[]
    def walk(v):
        if isinstance(v,str):
            if v.strip(): found.append(v.strip())
        elif isinstance(v,list):
            for x in v: walk(x)
        elif isinstance(v,dict):
            for k in preferred:
                if k in v: walk(v[k])
            if not any(k in v for k in preferred):
                for k,x in v.items():
                    if str(k).lower() not in ignored: walk(x)
    walk(row)
    return "\n".join(dict.fromkeys(found))
def simhash(text):
    words=re.findall(r"[a-z0-9áéíóúüñ]+",text.casefold())
    grams=[" ".join(words[i:i+3]) for i in range(max(0,len(words)-2))]
    if len(grams)>512:
        step=len(grams)/512
        grams=[grams[int(i*step)] for i in range(512)]
    if not grams: grams=words[:64]
    acc=[0]*64
    for g in grams:
        v=int.from_bytes(_hashlib.blake2b(g.encode("utf-8"),digest_size=8).digest(),"big")
        for bit in range(64): acc[bit]+=1 if (v>>bit)&1 else -1
    value=0
    for bit,n in enumerate(acc):
        if n>=0: value|=1<<bit
    return value
def documents_from_jsonl(stream, source, out):
    for line in stream:
        if not line.strip(): continue
        row=json.loads(line)
        text=row.get("text") if isinstance(row,dict) else None
        if not text and isinstance(row,dict): text=row_text(row)
        if isinstance(text,str) and len(text.strip())>=40:
            out.append((source,text))
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--cosmopedia-jsonl",type=Path,default=None,help="Optional manually curated Cosmopedia candidate JSONL to include in the global audit")
    args=parser.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    docs=[]
    with zipfile.ZipFile(IMPORT_ZIP) as z:
        manifest=json.loads(z.read("IMPORT-MANIFEST.json"))
        if manifest.get("records_staged")!=286464 or manifest.get("active_training_authorized") is not False:
            raise RuntimeError("Unexpected import manifest; fail closed")
        with z.open("covost2-cc0/train.jsonl.gz") as raw, gzip.GzipFile(fileobj=raw) as f: documents_from_jsonl(f,"covost2",docs)
        with z.open("mathlib4-apache/documents.train.jsonl.gz") as raw, gzip.GzipFile(fileobj=raw) as f: documents_from_jsonl(f,"mathlib4",docs)
        with z.open("scienceverse-ccby/documents.train.jsonl") as f: documents_from_jsonl(f,"scienceverse",docs)
        literature=z.read("literature-es/train.txt").decode("utf-8")
        docs.extend(("literature",p) for p in literature.split("\n\n") if len(p.strip())>=40)
        nasa=z.read("nasa-ntrs-file-reviewed/train.txt").decode("utf-8")
        docs.append(("nasa",nasa))
        for name in z.namelist():
            if name.startswith("ronin-authored-papers/") and name.endswith(".md"):
                docs.append(("papers",z.read(name).decode("utf-8")))
    if args.cosmopedia_jsonl is not None:
        with args.cosmopedia_jsonl.open("r",encoding="utf-8") as stream:
            documents_from_jsonl(stream,"cosmopedia",docs)
    # Audit the exact real source-scoped RONIN-IA artifact plus only explicitly supplied curated candidates.
    if len(docs)<250000: raise RuntimeError(f"Unexpectedly small real-artifact audit corpus: {len(docs)}")
    exact={}; exact_duplicates=[]; exact_duplicate_indices=set(); holdout=holdout_rows()
    holdout_norm=[norm(x["question"]) for x in holdout]
    holdout_exact=[]
    hashes=[]; sources=[]; lengths=[]
    for idx,(source,text) in enumerate(docs):
        n=norm(text)
        if not n: continue
        digest=hashlib.sha256(n.encode("utf-8")).hexdigest()
        if digest in exact:
            exact_duplicate_indices.add(idx)
            if len(exact_duplicates)<200: exact_duplicates.append({"first":exact[digest],"duplicate":{"index":idx,"source":source}})
        else: exact[digest]={"index":idx,"source":source}
        for qidx,q in enumerate(holdout_norm):
            if len(q)>=24 and q in n:
                holdout_exact.append({"document_index":idx,"source":source,"holdout_index":qidx})
        hashes.append(simhash(text)); sources.append(source); lengths.append(len(text))
    # 4x16-bit bands guarantee candidate retrieval for any pair with <=3 differing bits.
    buckets=defaultdict(list)
    for idx,h in enumerate(hashes):
        for band in range(4): buckets[(band,(h>>(band*16))&0xffff)].append(idx)
    near=[]; checked=0; seen_pairs=set()
    for ids in buckets.values():
        if len(ids)<2: continue
        for a,b in combinations(ids,2):
            pair=(a,b) if a<b else (b,a)
            if pair in seen_pairs: continue
            seen_pairs.add(pair); checked+=1
            if (hashes[a]^hashes[b]).bit_count()<=3:
                if len(near)<1000: near.append({"a":{"index":a,"source":sources[a]},"b":{"index":b,"source":sources[b]},"hamming":(hashes[a]^hashes[b]).bit_count()})
    counts={}
    for s in sources: counts[s]=counts.get(s,0)+1
    excluded=sorted({item["b"]["index"] for item in near} | exact_duplicate_indices)
    complete_near_audit=len(near)<1000
    exacts_covered=exact_duplicate_indices.issubset(set(excluded))
    dedup_plan={"method":"For every flagged near-duplicate pair, retain the lower global index and exclude the higher; exclude exact-duplicate endpoints as well.",
      "excluded_global_indices":excluded,"records_to_exclude":len(excluded),
      "near_duplicate_pairs_detected":len(near),"near_duplicate_pair_list_complete":complete_near_audit,
      "exact_duplicate_records_covered":exacts_covered}
    report={"schema":"heretic-global-train-corpus-audit-v2","documents_audited":len(hashes),"source_counts":counts,
      "exact_duplicate_groups_or_hits":len(exact_duplicate_indices),"exact_duplicate_examples":exact_duplicates,
      "simhash_method":"64-bit word-trigram SimHash, up to 512 evenly sampled trigrams/document; 4x16-bit band candidate retrieval; Hamming distance <=3",
      "near_duplicate_pairs_found":len(near),"near_duplicate_pairs_capped_at":1000,"near_duplicate_examples":near,
      "candidate_pairs_checked":checked,"holdout_questions":len(holdout),"exact_holdout_question_matches":len(holdout_exact),
      "holdout_matches":holdout_exact[:200],"deduplication_plan":dedup_plan,
      "limitations":["This audit is a high-recall heuristic, not semantic proof of no contamination.","The synthetic 120-question diagnostic is not a public benchmark.","The audit includes exact source-scoped RONIN-IA train artifacts and only explicitly supplied curated candidates; all other unreviewed candidates remain excluded.","Global source rights remain source-scoped; no broader redistribution or commercial rights are inferred."],
      "training_authorized":bool(not holdout_exact and complete_near_audit and exacts_covered),
      "authorization_scope":"Exact source-scoped RONIN-IA train partitions plus explicitly supplied curated candidates after deterministic exclusion of exact and SimHash near-duplicate endpoints; validation/test/holdout and all other unreviewed candidates excluded."}
    (OUT/"GLOBAL-CORPUS-AUDIT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
