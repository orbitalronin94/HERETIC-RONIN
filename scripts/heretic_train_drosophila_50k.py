#!/usr/bin/env python3
"""Corpus-only 500M experiment on the 50k Drosophila JSONL shards."""

from __future__ import annotations

import hashlib
import json
import os
import time
from pathlib import Path
from typing import Any

import torch

from ronin.config import ModelConfig, TrainingConfig
from ronin.data.batches import NextTokenBatches, encode_text_file
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer
from ronin.training.loop import train
from ronin.utils.repro import seed_everything

DATA_ROOT = Path("data/drosophila/parts")
OUT_ROOT = Path("reports/drosophila-50k-500m")
EXPECTED_SHARDS = 10
EXPECTED_ROWS = 50_000
PREFERRED_FIELDS = (
    "domain", "skill", "difficulty", "language",
    "prompt", "instruction", "question", "input", "problem",
    "response", "answer", "completion", "output", "solution",
    "explanation", "reasoning", "assumptions", "verification", "text", "content",
)
IGNORED_FIELDS = {
    "id", "uid", "domain_id", "family_id", "scenario_id",
    "split", "status", "license", "source", "metadata", "tags",
}


def leaf_text(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value.strip()] if value.strip() else []
    if isinstance(value, list):
        return [part for item in value for part in leaf_text(item)]
    if isinstance(value, dict):
        found: list[str] = []
        for key in PREFERRED_FIELDS:
            if key in value:
                found.extend(leaf_text(value[key]))
        if found:
            return found
        for key, child in value.items():
            if str(key).lower() not in IGNORED_FIELDS:
                found.extend(leaf_text(child))
        return found
    return []


def row_to_text(row: Any) -> str:
    parts = leaf_text(row)
    if not parts:
        raise ValueError("JSONL row contains no usable textual training fields")
    # Preserve field order; remove repeated identical strings within one row.
    unique = list(dict.fromkeys(parts))
    return "\n".join(unique)


def collect_corpus() -> dict[str, Any]:
    shards = sorted(DATA_ROOT.glob("*.jsonl"))
    if len(shards) != EXPECTED_SHARDS:
        raise RuntimeError(f"expected {EXPECTED_SHARDS} JSONL shards, found {len(shards)}")
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    target = OUT_ROOT / "corpus.txt"
    dataset_digest = hashlib.sha256()
    seen_ids: set[str] = set()
    seen_rows: set[str] = set()
    seen_text: set[str] = set()
    duplicate_rows = 0
    duplicate_text = 0
    total_rows = 0
    shard_reports = []

    with target.open("w", encoding="utf-8") as dst:
        for shard in shards:
            shard_digest = hashlib.sha256()
            shard_rows = 0
            with shard.open("rb") as src:
                for line_number, raw_line in enumerate(src, 1):
                    if not raw_line.strip():
                        continue
                    shard_digest.update(raw_line)
                    dataset_digest.update(raw_line)
                    try:
                        row = json.loads(raw_line)
                    except json.JSONDecodeError as exc:
                        raise ValueError(f"invalid JSON in {shard}:{line_number}: {exc}") from exc
                    if not isinstance(row, dict):
                        raise ValueError(f"expected JSON object in {shard}:{line_number}")
                    shard_rows += 1
                    total_rows += 1
                    row_id = row.get("id")
                    if row_id is not None:
                        normalized_id = str(row_id)
                        if normalized_id in seen_ids:
                            raise ValueError(f"duplicate record id: {normalized_id}")
                        seen_ids.add(normalized_id)
                    canonical = json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                    row_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
                    if row_hash in seen_rows:
                        duplicate_rows += 1
                    seen_rows.add(row_hash)
                    text = row_to_text(row)
                    normalized_text = " ".join(text.split())
                    if normalized_text in seen_text:
                        duplicate_text += 1
                    seen_text.add(normalized_text)
                    dst.write(text + "\n\n")
            if shard_rows != 5_000:
                raise RuntimeError(f"{shard.name}: expected 5000 rows, found {shard_rows}")
            shard_reports.append({
                "file": shard.name,
                "rows": shard_rows,
                "bytes": shard.stat().st_size,
                "sha256": shard_digest.hexdigest(),
            })

    if total_rows != EXPECTED_ROWS:
        raise RuntimeError(f"expected {EXPECTED_ROWS} rows, found {total_rows}")
    text_bytes = target.stat().st_size
    if text_bytes < 1_000_000:
        raise RuntimeError(f"unexpectedly small training text: {text_bytes} bytes")
    return {
        "source": str(DATA_ROOT),
        "rows": total_rows,
        "unique_ids": len(seen_ids),
        "exact_duplicate_rows": duplicate_rows,
        "duplicate_normalized_text_rows": duplicate_text,
        "unique_normalized_text_rows": len(seen_text),
        "text_bytes": text_bytes,
        "dataset_sha256": dataset_digest.hexdigest(),
        "shards": shard_reports,
        "note": "50k are procedurally generated train candidates; parameterized rows are not 50k independent capabilities.",
    }


def main() -> None:
    seed = int(os.environ["EXPERIMENT_SEED"])
    steps = int(os.environ.get("TRAINING_STEPS", "100"))
    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4")))
    torch.set_num_interop_threads(1)
    seed_everything(seed)

    OUT = OUT_ROOT / f"seed-{seed}"
    OUT.mkdir(parents=True, exist_ok=True)
    corpus = collect_corpus()
    tokens = encode_text_file(OUT_ROOT / "corpus.txt", ByteTokenizer())

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
        raise AssertionError(f"expected 500102144 parameters, got {parameters}")

    training_config = TrainingConfig(
        batch_size=1,
        gradient_accumulation_steps=1,
        learning_rate=1.0e-4,
        min_learning_rate=1.0e-4,
        weight_decay=0.01,
        warmup_steps=5,
        max_steps=steps,
        grad_clip_norm=1.0,
        seed=seed,
        precision="fp32",
        checkpoint_every=steps,
    )
    batches = NextTokenBatches(tokens, 1, model_config.context_length, seed)
    metrics_path = OUT / "training-metrics.json"
    started = time.perf_counter()
    losses = train(
        model,
        batches,
        training_config,
        device="cpu",
        checkpoint_dir=OUT / "full-checkpoints",
        metrics_path=metrics_path,
        optimizer_mode="default",
    )
    elapsed = time.perf_counter() - started

    checkpoint = OUT / f"student-500m-seed-{seed}-step-{steps:08d}.pt"
    torch.save({
        "model": model.state_dict(),
        "model_config": model_config.__dict__,
        "step": steps,
        "parameter_count": parameters,
        "seed": seed,
        "initialization": "fresh_random_initialization",
        "dataset_sha256": corpus["dataset_sha256"],
        "tutor_used": False,
    }, checkpoint)
    for full_checkpoint in (OUT / "full-checkpoints").glob("*.pt"):
        full_checkpoint.unlink()
    (OUT / "full-checkpoints").rmdir()

    report = {
        "experiment": "drosophila-50k-500m-corpus-only",
        "seed": seed,
        "steps_completed": len(losses),
        "target_steps": steps,
        "student_parameters": parameters,
        "architecture": model_config.__dict__,
        "initial_loss": losses[0] if losses else None,
        "final_loss": losses[-1] if losses else None,
        "elapsed_seconds": elapsed,
        "checkpoint": str(checkpoint),
        "checkpoint_bytes": checkpoint.stat().st_size,
        "corpus": corpus,
        "tutor_used": False,
        "starting_weights": "fresh random initialization; existing main/checkpoints are not modified",
        "interpretation": "training-loss and reproducibility smoke experiment only; no held-out capability claim.",
    }
    (OUT / "experiment.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
