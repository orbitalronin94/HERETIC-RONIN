#!/usr/bin/env python3
"""HERETIC first 500M-parameter CPU smoke run: 100 next-token steps."""

from __future__ import annotations

import gzip
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import torch

from ronin.config import ModelConfig, TrainingConfig
from ronin.data.batches import NextTokenBatches, encode_text_file
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer
from ronin.training.loop import train
from ronin.utils.repro import seed_everything

ROOT = Path("payload/data/datasets/admitted")
OUT = Path("reports/first-500m")
MAX_TEXT_BYTES = 96 * 1024 * 1024
EXTENSIONS = {".txt", ".md", ".rst", ".lean", ".py", ".csv", ".tsv", ".jsonl"}


def strings(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        if value.strip():
            found.append(value)
    elif isinstance(value, dict):
        preferred = ("text", "content", "document", "body", "source", "target", "translation", "completion", "prompt")
        for key in preferred:
            if key in value:
                found.extend(strings(value[key]))
        if not found:
            for child in value.values():
                if isinstance(child, (str, list, dict)):
                    found.extend(strings(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(strings(child))
    return found


def collect_corpus() -> dict[str, Any]:
    if not ROOT.is_dir():
        raise FileNotFoundError(f"admitted corpus missing: {ROOT}")
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "corpus.txt"
    digest = hashlib.sha256()
    total = 0
    files = 0
    with target.open("w", encoding="utf-8") as dst:
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or path.name.lower() in {"manifest.json", "readme.md", "license", "license.txt"}:
                continue
            suffixes = path.suffixes
            is_gzip = suffixes and suffixes[-1] == ".gz"
            base_suffix = suffixes[-2] if is_gzip and len(suffixes) > 1 else (suffixes[-1] if suffixes else "")
            if base_suffix not in EXTENSIONS:
                continue
            try:
                raw = gzip.open(path, "rb").read() if is_gzip else path.read_bytes()
                text = raw.decode("utf-8", errors="replace")
                if base_suffix == ".jsonl":
                    chunks: list[str] = []
                    for line in text.splitlines():
                        try:
                            chunks.extend(strings(json.loads(line)))
                        except json.JSONDecodeError:
                            continue
                    text = "\n".join(chunks)
                if not text.strip():
                    continue
                encoded = (text + "\n\n").encode("utf-8")
                remaining = MAX_TEXT_BYTES - total
                if remaining <= 0:
                    break
                encoded = encoded[:remaining]
                dst.write(encoded.decode("utf-8", errors="ignore"))
                digest.update(encoded)
                total += len(encoded)
                files += 1
            except (OSError, EOFError):
                continue
    if total < 128 * 1024:
        raise RuntimeError(f"too little admitted text collected: {total} bytes")
    return {"source_root": str(ROOT), "files_used": files, "text_bytes": total, "text_sha256": digest.hexdigest(), "cap_bytes": MAX_TEXT_BYTES}


def main() -> None:
    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4")))
    torch.set_num_interop_threads(1)
    seed = 20261106
    seed_everything(seed)

    corpus = collect_corpus()
    tokenizer = ByteTokenizer()
    tokens = encode_text_file(OUT / "corpus.txt", tokenizer)
    model_config = ModelConfig(
        vocab_size=ByteTokenizer.vocab_size,
        context_length=128,
        n_layers=39,
        n_heads=16,
        d_model=1024,
        d_ff=2806,
        dropout=0.0,
        bias=False,
    )
    model = RoninLM(model_config)
    parameters = model.parameter_count
    if parameters != 500_102_144:
        raise AssertionError(f"unexpected student parameter count: {parameters}")

    training_config = TrainingConfig(
        batch_size=1,
        gradient_accumulation_steps=1,
        learning_rate=1.0e-4,
        min_learning_rate=1.0e-4,
        weight_decay=0.01,
        warmup_steps=5,
        max_steps=100,
        grad_clip_norm=1.0,
        seed=seed,
        precision="fp32",
        checkpoint_every=100,
    )
    training_config.validate()
    batches = NextTokenBatches(tokens, training_config.batch_size, model_config.context_length, seed)
    checkpoint_dir = OUT / "checkpoints"
    metrics_path = OUT / "training-metrics.json"
    losses = train(
        model,
        batches,
        training_config,
        device="cpu",
        checkpoint_dir=checkpoint_dir,
        metrics_path=metrics_path,
        optimizer_mode="default",
    )
    full_checkpoints = list(checkpoint_dir.glob("step-*.pt"))
    student_checkpoint = OUT / "student-500m-step-00000100.pt"
    torch.save({
        "model": model.state_dict(),
        "model_config": model_config.__dict__,
        "step": 100,
        "parameter_count": parameters,
        "seed": seed,
        "initialization": "fresh_random_initialization",
    }, student_checkpoint)
    for full_checkpoint in full_checkpoints:
        full_checkpoint.unlink()

    report = {
        "experiment": "heretic-500m-first-100-steps",
        "student_parameters": parameters,
        "architecture": {
            "vocab_size": model_config.vocab_size,
            "context_length": model_config.context_length,
            "layers": model_config.n_layers,
            "heads": model_config.n_heads,
            "width": model_config.d_model,
            "feed_forward_width": model_config.d_ff,
        },
        "steps_completed": len(losses),
        "student_checkpoint": str(student_checkpoint),
        "student_checkpoint_bytes": student_checkpoint.stat().st_size,
        "initial_loss": losses[0] if losses else None,
        "final_loss": losses[-1] if losses else None,
        "corpus": corpus,
        "tutor_used_for_these_100_steps": False,
        "interpretation": "Architecture and CPU-training smoke run only; not an instruction-tuning or held-out capability claim.",
        "seed": seed,
    }
    (OUT / "experiment.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
