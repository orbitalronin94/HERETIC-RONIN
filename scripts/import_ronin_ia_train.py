#!/usr/bin/env python3
"""Build a source-scoped RONIN-IA train import bundle; never imports eval splits."""
from __future__ import annotations
import gzip, hashlib, json, shutil
from pathlib import Path

ROOT = Path("source")
OUT = Path("staging/ronin-ia-train")
def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()
def verify(path: Path, expected: str):
    actual=sha(path)
    if actual != expected: raise SystemExit(f"SHA256 mismatch {path}: {actual} != {expected}")
def copy(src: Path, dst: Path):
    dst.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(src,dst)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    sources=[]
    # CoVoST: exact source-scoped CC0 train partition only.
    p=ROOT/"data/datasets/admitted/covost2-cc0-translation-only/train.jsonl.gz"
    verify(p,"771e6845e0097554398de8d3416e3effeb3c173cff341f037ac5437ea6344623")
    q=OUT/"covost2-cc0/train.jsonl.gz"; copy(p,q)
    sources.append({"id":"covost2-cc0-translation-only","records":270244,"license":"CC0-1.0","split":"train","sha256":sha(q),"bytes":q.stat().st_size,"status":"staged_train_source_scoped","note":"Translation target text only; preserve language-pair metadata; global G-0/holdout gates pending."})
    # ScienceVerse: retrieve the already audited train-only artifact, never the 7,365-row source payload.
    p=Path("scienceverse-artifact/documents.train.jsonl")
    verify(p,"bc09ca772a9fc3b5c3be0de10d1ee83beea1bf29f2b403d1e56b36049afc49dc")
    q=OUT/"scienceverse-ccby/documents.train.jsonl"; copy(p,q)
    sources.append({"id":"scienceverse-ccby-v1","records":7103,"held_excluded":262,"license":"CC-BY-4.0 / CC0 per document","split":"train","sha256":sha(q),"bytes":q.stat().st_size,"status":"staged_train_source_scoped","note":"Exact verified train-only audit artifact; global near-duplicate and holdout contamination gates pending."})
    # Spanish literature: source artifact is pinned by the manifest; select train.txt only.
    p=Path("literature-artifact/train.txt")
    verify(p,"9cd5d7e83ed7690713add22c40fdf35eaf1fb88da3dafb748ca8201b08df9a78")
    q=OUT/"literature-es/train.txt"; copy(p,q)
    sources.append({"id":"literature-es-v1","records":608,"license":"per-source; see RONIN-IA manifest","split":"train","sha256":sha(q),"bytes":q.stat().st_size,"status":"staged_train_source_scoped","note":"Validation and test files deliberately excluded."})
    # Mathlib4: exact audited train-only artifact from the pinned RONIN-IA run.
    p=Path("mathlib-artifact/train.txt")
    verify(p,"7c82a4d1e0f3788d6038002b41ae1ead1bf6a16cbf4e332f59f015501325667c")
    q=OUT/"mathlib4-apache/train.txt"; copy(p,q)
    gz=Path("mathlib-artifact/documents.train.jsonl.gz")
    verify(gz,"d7f86547d8607d13ee5e64320b8588b76914baffa95e8145f943c42d17d54958")
    qgz=OUT/"mathlib4-apache/documents.train.jsonl.gz"; copy(gz,qgz)
    sources.append({"id":"mathlib4-v1","records":8498,"license":"Apache-2.0","split":"train","sha256":sha(q),"bytes":q.stat().st_size,"jsonl_gzip_sha256":sha(qgz),"jsonl_gzip_bytes":qgz.stat().st_size,"status":"staged_train_source_scoped","note":"Exact audited train-only artifact from RONIN-IA run 42026633643; validation/test excluded; global G-0 remains FAIL."})
    # NASA: individually reviewed train payload only.
    p=ROOT/"data/datasets/admitted/nasa-ntrs-file-reviewed-v1/train.txt"
    verify(p,"874c77ef785236ce726a89a217b450684f36b82402b35174d9bbf3328249d1f8")
    q=OUT/"nasa-ntrs-file-reviewed/train.txt"; copy(p,q)
    sources.append({"id":"nasa-ntrs-file-reviewed-v1","records":2,"license":"NASA public-use/file-reviewed scope","split":"train","sha256":sha(q),"bytes":q.stat().st_size,"status":"staged_train_source_scoped","note":"Only two individually reviewed payloads; four mismatched attestations excluded."})
    # Owner-authorized Papers: exact pinned revision and the nine manifest-listed markdown payloads.
    manifest=json.loads((ROOT/"data/datasets/admitted/ronin-authored-papers-v1/manifest.json").read_text())
    paper_root=Path("papers-source")
    records=manifest.get("records",[])
    if len(records)!=9: raise SystemExit(f"expected 9 Papers manifest records, got {len(records)}")
    total=0
    for rec in records:
        rel=rec["payload"]["path"]; source_path=rec["source"]["path"]; expected=rec["payload"]["sha256"]
        src=paper_root/source_path
        # Some manifest entries omit the literal leading "# " present in the Git filename.
        if not src.exists() and not source_path.startswith("# "):
            prefixed=paper_root/("# "+source_path)
            if prefixed.exists(): src=prefixed
        verify(src,expected)
        dst=OUT/"ronin-authored-papers"/Path(rel).name; copy(src,dst); total+=dst.stat().st_size
    sources.append({"id":"ronin-authored-papers-v1","records":9,"license":"owner-authorized for internal RONIN training only","split":"train","bytes":total,"status":"staged_train_source_scoped","note":"No external redistribution or commercial rights inferred; nine Markdown files only, README excluded."})
    # Explicitly document sources that cannot yet be materialized.
    sources.extend([
      {"id":"meta-math/MetaMathQA","records":None,"status":"candidate_not_imported","note":"License and lineage/revision gates remain unresolved."},
      {"id":"amazon-science/street-reasoning","records":None,"status":"candidate_not_imported","note":"Apache-2.0 repo code does not establish rights for upstream dataset content."}
    ])
    summary={"schema_version":1,"source_repository":"orbitalronin94/RONIN-IA","source_ref":"main at workflow checkout; per-source immutable revisions and hashes retained in source manifests","status":"staged_train_not_active_training","global_g0":"FAIL","global_near_duplicate":"PENDING","benchmark_holdout_contamination":"PENDING","active_training_authorized":False,"records_staged":sum(x.get("records") or 0 for x in sources if x["status"]=="staged_train_source_scoped"),"expected_source_scoped_records":286464,"source_inventory_reconciliation":"RONIN-IA README reports 286,468, but exact pinned NASA train artifact contains 2 records (not 6); 4 reviewed records are held for payload/attestation mismatch. This importer therefore stages 286,464 exact train records.","sources":sources,"policy":"Staging preserves only source-scoped train payloads. No validation/test/holdout files are included. Do not feed this bundle to the model until global gates pass and task-specific adapters are reviewed."}
    (OUT/"IMPORT-MANIFEST.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
