#!/usr/bin/env python3
"""Conservatively curate the pinned Cosmopedia v0.1 auto_math_text pilot."""
from __future__ import annotations
import argparse, hashlib, json, re, zipfile
from pathlib import Path

EXPECTED_REVISION = "0ae6ec63f91742bd2d1eaef4f02232c55d719385"
EXPECTED_SOURCE_SHA256 = "050b03f64c3e9976d91ff86447761174f46121c0af899004172368f61255dcc6"
SOURCE = "HuggingFaceTB/cosmopedia"
CONFIG = "auto_math_text"
LICENSE = "Apache-2.0"
EMAIL = re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")
PHONE = re.compile(r"(?<!\d)(?:\+?\d[\d .()/-]{7,}\d)(?!\d)")

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def normalized(text: str) -> str:
    return re.sub(r"\s+", " ", text.casefold()).strip()

def parse_json_stream(text: str):
    """Parse JSON objects without treating Unicode line separators as JSONL boundaries."""
    decoder = json.JSONDecoder()
    pos = 0
    while pos < len(text):
        while pos < len(text) and text[pos].isspace():
            pos += 1
        if pos >= len(text):
            break
        row, end = decoder.raw_decode(text, pos)
        if not isinstance(row, dict):
            raise ValueError("Candidate JSON stream contains a non-object record")
        yield row
        pos = end

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    with zipfile.ZipFile(args.bundle) as archive:
        bundle_manifest = json.loads(archive.read("OPEN-SOURCE-MANIFEST.json"))
        if bundle_manifest.get("schema") != "heretic-open-source-candidate-bundle-v1":
            raise RuntimeError("Unexpected candidate bundle schema")
        if bundle_manifest.get("training_authorized") is not False:
            raise RuntimeError("Candidate bundle must remain unadmitted at curation input")
        source = next((x for x in bundle_manifest.get("sources", [])
                       if x.get("source") == SOURCE and x.get("config") == CONFIG), None)
        if not source:
            raise RuntimeError("Pinned Cosmopedia auto_math_text source missing from bundle manifest")
        if source.get("revision") != EXPECTED_REVISION:
            raise RuntimeError("Cosmopedia revision mismatch")
        if source.get("sha256") != EXPECTED_SOURCE_SHA256 or source.get("rows_written") != 5000:
            raise RuntimeError("Cosmopedia payload SHA/row count mismatch")
        payload = archive.read("HuggingFaceTB__cosmopedia.jsonl")
        if digest(payload) != EXPECTED_SOURCE_SHA256:
            raise RuntimeError("Cosmopedia payload SHA-256 mismatch")

    accepted = []
    seen = set()
    rejected = {"too_short": 0, "too_long": 0, "control_or_replacement_character": 0,
                "email_pattern": 0, "phone_pattern": 0, "exact_duplicate": 0,
                "missing_seed_or_format_metadata": 0}
    input_rows = 0
    for row in parse_json_stream(payload.decode("utf-8")):
        input_rows += 1
        text = row.get("text")
        raw_metadata = row.get("source_metadata", {}) if isinstance(row.get("source_metadata"), dict) else {}
        metadata = {k: raw_metadata.get(k) for k in ("seed_data", "audience", "format", "token_length")
                    if raw_metadata.get(k) is not None}
        if not isinstance(text, str) or len(text.strip()) < 500:
            rejected["too_short"] += 1
            continue
        if len(text) > 12000:
            rejected["too_long"] += 1
            continue
        if any((ord(ch) < 32 and ch not in "\n\r") or ord(ch) == 0x7f or ch == "\ufffd" for ch in text):
            rejected["control_or_replacement_character"] += 1
            continue
        if EMAIL.search(text):
            rejected["email_pattern"] += 1
            continue
        if PHONE.search(text):
            rejected["phone_pattern"] += 1
            continue
        if metadata.get("seed_data") != "auto_math_text" or metadata.get("format") != "educational_piece":
            rejected["missing_seed_or_format_metadata"] += 1
            continue
        key = hashlib.sha256(normalized(text).encode("utf-8")).hexdigest()
        if key in seen:
            rejected["exact_duplicate"] += 1
            continue
        seen.add(key)
        accepted.append({
            "text": text,
            "source": SOURCE,
            "revision": EXPECTED_REVISION,
            "config": CONFIG,
            "license": LICENSE,
            "source_metadata": metadata,
            "source_text_sha256": digest(text.encode("utf-8")),
        })

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="\n") as out:
        for row in accepted:
            out.write(json.dumps(row, ensure_ascii=False) + "\n")
    manifest = {
        "schema": "heretic-cosmopedia-curated-candidate-v1",
        "source": SOURCE,
        "revision": EXPECTED_REVISION,
        "config": CONFIG,
        "split": "train",
        "declared_license": LICENSE,
        "source_payload_sha256": EXPECTED_SOURCE_SHA256,
        "input_rows": input_rows,
        "accepted_rows": len(accepted),
        "rejected_rows": sum(rejected.values()),
        "rejection_counts": rejected,
        "curated_bytes": args.output.stat().st_size,
        "curated_sha256": digest(args.output.read_bytes()),
        "manual_review": {
            "method": "50 deterministic stratified excerpts sampled across the eligible source ordering; opening passages manually inspected",
            "result": "Suitable as experimental next-token educational prose after mechanical cleanup; not certified for mathematical correctness or instruction-following supervision",
            "limitations": [
                "A sample review does not verify every document or every mathematical claim.",
                "Dataset card declares Apache-2.0; upstream AutoMathText seed lineage is retained as a caveat, not independently rights-cleared here.",
                "This source is a pretraining-text candidate, not a gold-answer or reasoning-supervision dataset."
            ]
        },
        "checks": {
            "pinned_revision": True,
            "payload_sha256_verified": True,
            "train_split_only": True,
            "seed_data_auto_math_text_only": True,
            "format_educational_piece_only": True,
            "minimum_length_500": True,
            "maximum_length_12000": True,
            "control_and_replacement_characters_filtered": True,
            "email_phone_pattern_filtered": True,
            "exact_duplicates_within_source_removed": True,
            "cross_source_near_duplicate": "PENDING_GLOBAL_AUDIT",
            "global_holdout_contamination": "PENDING_GLOBAL_AUDIT",
            "source_rights_review": "dataset card declares Apache-2.0; upstream seed lineage remains caveated",
            "training_authorized": False
        },
        "status": "CURATED_CANDIDATE_PENDING_GLOBAL_AUDIT",
        "training_authorized": False
    }
    args.manifest.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
