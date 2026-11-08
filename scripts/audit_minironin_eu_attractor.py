#!/usr/bin/env python3
"""Forensic scan for unexpected EU/Brussels lexical attractors in training sources."""
from __future__ import annotations
import gzip, json, re, zipfile
from collections import Counter, defaultdict
from pathlib import Path

PATTERNS = {
    "parlamento_europeo": re.compile(r"parlamento\\s+europeo", re.I),
    "bruselas": re.compile(r"bruselas", re.I),
    "union_europea": re.compile(r"uni[oó]n\\s+europea", re.I),
    "sigla_ue": re.compile(r"\\bUE\\b"),
    "comision_europea": re.compile(r"comisi[oó]n\\s+europea", re.I),
    "europa_europeo": re.compile(r"\\beurop(?:a|eo|ea|eos|eas)\\b", re.I),
}
TEXT_SUFFIXES = {".md",".txt",".json",".jsonl",".ndjson",".csv",".tsv",".xml",".html",".htm",".yaml",".yml",".py",".toml",".rst",".tex",".log"}

def scan_text(source, text, results, totals):
    counts = {name: len(rx.findall(text)) for name,rx in PATTERNS.items()}
    for name,n in counts.items(): totals[name] += n
    if any(counts.values()):
        snippets=[]
        lines=text.splitlines()
        for i,line in enumerate(lines):
            found=[name for name,rx in PATTERNS.items() if rx.search(line)]
            if found and len(snippets)<30:
                snippets.append({"line":i+1,"terms":found,"text":line[:500]})
        results.append({"source":source,"counts":counts,"snippets":snippets})

def main():
    root=Path(".")
    totals=Counter(); results=[]; scanned=[]
    # Exact unpacked training source files (HERETIC + PRODATPHIL) and repo-side generators/docs.
    for base in [root/"corpus-unpacked", root/"prodatphil-unpacked", root/"minironin"]:
        if not base.exists(): continue
        for p in sorted(base.rglob("*")):
            if not p.is_file() or p.suffix.lower() not in TEXT_SUFFIXES and not p.name.lower().endswith((".jsonl.gz",".txt.gz",".md.gz")): continue
            try:
                raw=p.read_bytes()
                if p.name.lower().endswith(".gz"): raw=gzip.decompress(raw)
                text=raw.decode("utf-8",errors="replace")
            except Exception as exc:
                scanned.append({"path":str(p),"error":str(exc)}); continue
            scan_text(str(p),text,results,totals)
            scanned.append({"path":str(p),"bytes":p.stat().st_size})
    report={
      "schema":"minironin-eu-attractor-forensic-audit-v1",
      "files_scanned":len(scanned),
      "files_with_matches":len(results),
      "term_totals":dict(totals),
      "matches_by_file":sorted(results,key=lambda x:sum(x["counts"].values()),reverse=True),
      "scanned_files":scanned,
      "scope":["HERETIC approved corpus release unpacked text files","PRODATPHIL v0.3 unpacked text files","MINIRONIN tracked source/docs/generators at audit checkout"],
      "limitations":["Counts are literal lexical matches, not token-frequency counts or proof of training exposure.","Binary formats and unsupported encodings are not semantically decoded.","The report distinguishes the public source tree from the exact training-time expanded dataset; generated datasets may need separate inclusion if not committed."]
    }
    out=Path("reports/eu-attractor-audit"); out.mkdir(parents=True,exist_ok=True)
    (out/"EU-ATTRACTOR-AUDIT.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\\n")
    summary=["# MINIRONIN EU-attractor forensic audit","",f"- Files scanned: {len(scanned)}",f"- Files with matches: {len(results)}","", "## Literal term counts",""]
    summary += [f"- {k}: {v}" for k,v in totals.items()]
    summary += ["","## Highest-hit files",""]
    for item in report["matches_by_file"][:30]:
        summary.append(f"- `{item['source']}`: "+", ".join(f"{k}={v}" for k,v in item["counts"].items() if v))
    (out/"SUMMARY.md").write_text("\\n".join(summary)+"\\n")
    print(json.dumps({"files_scanned":len(scanned),"files_with_matches":len(results),"term_totals":dict(totals),"top_files":[{"source":x["source"],"counts":x["counts"]} for x in report["matches_by_file"][:15]]},ensure_ascii=False,indent=2))
if __name__=="__main__": main()
