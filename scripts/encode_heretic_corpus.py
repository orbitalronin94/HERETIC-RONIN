#!/usr/bin/env python3
"""Encode separately audited train and validation JSONL files with a frozen tokenizer."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np
from tokenizers import Tokenizer

from build_heretic_tokenizer import extract_text


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def encode_files(paths: list[Path], tokenizer: Tokenizer, output: Path) -> tuple[int, int]:
    documents = tokens = 0
    with output.open("wb") as target:
        for path in paths:
            opener = gzip.open if path.suffix == ".gz" else open
            with opener(path, "rt", encoding="utf-8") as stream:
                for line_number, line in enumerate(stream, 1):
                    if not line.strip():
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError as exc:
                        raise ValueError(f"Invalid JSONL at {path}:{line_number}") from exc
                    text = extract_text(row)
                    if not text:
                        continue
                    ids = tokenizer.encode(text).ids
                    if not ids:
                        continue
                    if max(ids) >= 65536:
                        raise RuntimeError("Tokenizer ID exceeds uint16 storage")
                    np.asarray(ids, dtype="<u2").tofile(target)
                    documents += 1
                    tokens += len(ids)
    return documents, tokens


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tokenizer", required=True)
    parser.add_argument("--train", nargs="+", required=True)
    parser.add_argument("--validation", nargs="+", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    train_paths = [Path(p) for p in args.train]
    validation_paths = [Path(p) for p in args.validation]
    if {p.resolve() for p in train_paths} & {p.resolve() for p in validation_paths}:
        parser.error("Train and validation files must be disjoint")
    for path in train_paths + validation_paths:
        if not path.is_file() or path.stat().st_size == 0:
            parser.error(f"Missing or empty input: {path}")
    tokenizer_path = Path(args.tokenizer)
    tokenizer = Tokenizer.from_file(str(tokenizer_path))
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    train_docs, train_tokens = encode_files(train_paths, tokenizer, out / "train.bin")
    val_docs, val_tokens = encode_files(validation_paths, tokenizer, out / "validation.bin")
    if train_tokens < 1000 or val_tokens < 100:
        raise RuntimeError(f"Encoded partitions too small: train={train_tokens}, validation={val_tokens}")
    manifest = {
        "schema": "heretic-tokenized-corpus-v1",
        "tokenizer_sha256": digest(tokenizer_path),
        "train_files": [{"path": str(p), "sha256": digest(p), "bytes": p.stat().st_size} for p in train_paths],
        "validation_files": [{"path": str(p), "sha256": digest(p), "bytes": p.stat().st_size} for p in validation_paths],
        "train_documents": train_docs,
        "validation_documents": val_docs,
        "train_tokens": train_tokens,
        "validation_tokens": val_tokens,
        "dtype": "little-endian uint16",
        "validation_policy": "independent source-provided validation partition; never used to fit tokenizer",
    }
    (out / "encoding-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
