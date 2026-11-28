#!/usr/bin/env python3
"""Train a fresh byte-level BPE tokenizer using approved train-only JSONL records."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import unicodedata
from pathlib import Path
from typing import Iterator

from tokenizers import Tokenizer, Regex, decoders, models, normalizers, pre_tokenizers, processors, trainers


SPECIAL_TOKENS = ["<|unk|>", "<|bos|>", "<|eos|>", "<|pad|>"]
TEXT_KEYS = ("text", "content", "document", "body", "prompt", "response", "completion")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def extract_text(record: object) -> str:
    if isinstance(record, str):
        return unicodedata.normalize("NFC", record)
    if not isinstance(record, dict):
        return ""
    chunks = []
    for key in TEXT_KEYS:
        value = record.get(key)
        if isinstance(value, str) and value.strip():
            chunks.append(value)
    messages = record.get("messages")
    if isinstance(messages, list):
        for message in messages:
            if isinstance(message, dict) and isinstance(message.get("content"), str):
                chunks.append(message["content"])
    return unicodedata.normalize("NFC", "\n\n".join(chunks))


def iter_text(paths: list[Path]) -> Iterator[str]:
    for path in paths:
        opener = gzip.open if path.suffix == ".gz" else open
        with opener(path, "rt", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ValueError(f"Invalid JSONL at {path}:{line_number}") from exc
                text = extract_text(record)
                if text:
                    yield text


def build_tokenizer(paths: list[Path], vocab_size: int) -> Tokenizer:
    if vocab_size < 260:
        raise ValueError("vocab_size must be at least 260 for byte-level coverage")
    tokenizer = Tokenizer(models.BPE(unk_token="<|unk|>"))
    tokenizer.normalizer = normalizers.NFC()
    tokenizer.pre_tokenizer = pre_tokenizers.Sequence([
        pre_tokenizers.Split(Regex(r"[0-9]"), behavior="isolated"),
        pre_tokenizers.ByteLevel(add_prefix_space=False),
    ])
    tokenizer.decoder = decoders.ByteLevel()
    trainer = trainers.BpeTrainer(
        vocab_size=vocab_size,
        min_frequency=2,
        special_tokens=SPECIAL_TOKENS,
        initial_alphabet=pre_tokenizers.ByteLevel.alphabet(),
        show_progress=True,
    )
    tokenizer.train_from_iterator(iter_text(paths), trainer=trainer)
    if len(tokenizer.get_vocab()) != vocab_size:
        raise RuntimeError(
            f"Tokenizer learned {len(tokenizer.get_vocab())} entries; expected {vocab_size}. "
            "Increase the train corpus or lower the requested vocabulary explicitly."
        )
    eos_id = tokenizer.token_to_id("<|eos|>")
    tokenizer.post_processor = processors.TemplateProcessing(
        single="$A <|eos|>",
        pair="$A <|eos|> $B <|eos|>",
        special_tokens=[("<|eos|>", eos_id)],
    )
    tokenizer.enable_padding(pad_id=tokenizer.token_to_id("<|pad|>"), pad_token="<|pad|>")
    tokenizer.enable_truncation(max_length=512)
    return tokenizer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", nargs="+", required=True,
                        help="Approved train-only JSONL/JSONL.GZ files")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--vocab-size", type=int, default=32768)
    args = parser.parse_args()
    paths = [Path(item) for item in args.corpus]
    for path in paths:
        if not path.is_file() or path.stat().st_size == 0:
            parser.error(f"Missing or empty corpus file: {path}")
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    tokenizer = build_tokenizer(paths, args.vocab_size)
    tokenizer_path = out / "tokenizer.json"
    tokenizer.save(str(tokenizer_path))
    manifest = {
        "schema": "heretic-byte-bpe-v1",
        "algorithm": "BPE",
        "pretokenizer": "digits isolated + ByteLevel",
        "normalizer": "Unicode NFC",
        "vocab_size": len(tokenizer.get_vocab()),
        "special_tokens": {
            token: tokenizer.token_to_id(token) for token in SPECIAL_TOKENS
        },
        "corpus_files": [
            {"path": str(path), "bytes": path.stat().st_size,
             "sha256": sha256_file(path)} for path in paths
        ],
        "tokenizer_sha256": sha256_file(tokenizer_path),
        "training_scope": "approved train partitions only; validation and holdout excluded",
    }
    (out / "tokenizer-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
