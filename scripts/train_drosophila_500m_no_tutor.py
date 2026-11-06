#!/usr/bin/env python3
"""Continue the verified 500M HERETIC student on Drosophila 50k only; paired 64-item evaluation."""

from __future__ import annotations

import gc
import hashlib
import json
import os
import re
from collections import defaultdict
from dataclasses import replace
from pathlib import Path

import torch
from torch.nn import functional as F

from ronin.config import ModelConfig, TrainingConfig
from ronin.data.batches import NextTokenBatches, encode_text_file
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer
from ronin.training.loop import train
from ronin.utils.repro import seed_everything

from evaluate_mmlu_pro import (
    DATASET_REVISION,
    LABELS,
    format_prompt,
    load_external_dataset,
    rows_sha256,
    select_stratified,
)

ROOT = Path(".")
PARTS = ROOT / "data/drosophila/parts"
INCOMING = ROOT / "incoming/student-artifact"
OUT = ROOT / "reports/drosophila-50k-no-tutor-500m"
ARTIFACT_RUN_ID = 42220358202
ARTIFACT_NAME = "heretic-student-500m-first-100-steps"
EXPECTED_PARAMETERS = 500_102_144
EXPECTED_START_STEP = 100
ADDITIONAL_STEPS = 500
EVAL_LIMIT = 64
EVAL_SEED = 2026
EVAL_CONTEXT = 4096

SHARDS = [
    "01_matematicas_5000.jsonl",
    "02_algebra_5000.jsonl",
    "03_logica_5000.jsonl",
    "04_programacion_5000.jsonl",
    "05_fisica_5000.jsonl",
    "06_quimica_5000.jsonl",
    "07_probabilidad_5000.jsonl",
    "08_estadistica_5000.jsonl",
    "09_economia_5000.jsonl",
    "10_ingenieria_5000.jsonl",
]
DOMAINS = {
    "matematicas", "algebra", "logica", "programacion", "fisica",
    "quimica", "probabilidad", "estadistica", "economia", "ingenieria",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def build_drosophila_corpus() -> dict:
    """Read only the ten newly merged JSONL shards; reject anything outside their contract."""
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / "drosophila-50k-train.txt"
    digest = hashlib.sha256()
    counts = defaultdict(int)
    ids: set[int] = set()
    prompts: set[str] = set()
    rows_seen = 0

    with target.open("w", encoding="utf-8") as dst:
        for shard_name in SHARDS:
            path = PARTS / shard_name
            if not path.is_file():
                raise FileNotFoundError(f"Required Drosophila shard missing: {path}")
            shard_rows = 0
            with path.open("r", encoding="utf-8") as src:
                for line_number, line in enumerate(src, 1):
                    if not line.strip():
                        continue
                    row = json.loads(line)
                    if row.get("split") != "train_candidate":
                        raise ValueError(f"Non-training split in {shard_name}:{line_number}")
                    if row.get("origin") != "synthetic_procedural":
                        raise ValueError(f"Unexpected origin in {shard_name}:{line_number}")
                    if row.get("generator") != "heretic-drosophila-procedural-v1":
                        raise ValueError(f"Unexpected generator in {shard_name}:{line_number}")
                    domain = row.get("domain")
                    if domain not in DOMAINS:
                        raise ValueError(f"Unexpected domain {domain!r} in {shard_name}:{line_number}")
                    row_id = int(row["id"])
                    if row_id in ids:
                        raise ValueError(f"Duplicate sample ID: {row_id}")
                    ids.add(row_id)
                    prompt = str(row.get("prompt", "")).strip()
                    answer = str(row.get("answer", "")).strip()
                    reasoning = str(row.get("reasoning", "")).strip()
                    verification = str(row.get("verification", "")).strip()
                    if not prompt or not answer or not reasoning or not verification:
                        raise ValueError(f"Missing prompt/answer/reasoning/verification in {shard_name}:{line_number}")
                    normalized = re.sub(r"\s+", " ", prompt.casefold())
                    prompts.add(normalized)
                    assumptions = row.get("assumptions", [])
                    assumption_text = "; ".join(str(item) for item in assumptions if str(item).strip())
                    sample = (
                        f"DOMINIO: {domain}\n"
                        f"HABILIDAD: {row.get('skill', '')}\n"
                        f"DIFICULTAD: {row.get('difficulty', '')}\n"
                        f"PREGUNTA: {prompt}\n"
                        f"RESPUESTA: {answer}\n"
                        f"RAZONAMIENTO: {reasoning}\n"
                        f"VERIFICACION: {verification}\n"
                        f"SUPUESTOS: {assumption_text}\n\n"
                    )
                    encoded = sample.encode("utf-8")
                    dst.write(sample)
                    digest.update(encoded)
                    counts[domain] += 1
                    shard_rows += 1
                    rows_seen += 1
            if shard_rows != 5000:
                raise AssertionError(f"{shard_name}: expected 5000 rows, found {shard_rows}")

    expected_ids = set(range(1301, 51301))
    if rows_seen != 50_000 or ids != expected_ids:
        raise AssertionError(
            f"Expected exactly IDs 1301..51300 (50,000 rows), got {rows_seen} rows "
            f"and ID range {min(ids) if ids else None}..{max(ids) if ids else None}"
        )
    if set(counts) != DOMAINS or any(value != 5000 for value in counts.values()):
        raise AssertionError(f"Unexpected domain balance: {dict(counts)}")
    if len(prompts) < 49_000:
        raise AssertionError(f"Too few distinct prompts: {len(prompts)}")

    return {
        "dataset": "HERETIC-RONIN Drosophila 01301-51300",
        "shards": SHARDS,
        "rows": rows_seen,
        "ids": {"first": min(ids), "last": max(ids), "unique": len(ids)},
        "domain_counts": dict(sorted(counts.items())),
        "distinct_prompts": len(prompts),
        "text_bytes": target.stat().st_size,
        "text_sha256": digest.hexdigest(),
        "split": "train_candidate_only",
        "generator": "heretic-drosophila-procedural-v1",
        "other_training_sources_used": [],
        "tutor_used": False,
        "quality_limit": (
            "50,000 procedural parameterizations across 50 task families; "
            "row count does not imply 50,000 independent capabilities."
        ),
    }


def load_student_checkpoint() -> tuple[dict, ModelConfig]:
    candidates = list(INCOMING.rglob("student-500m-step-00000100.pt"))
    if len(candidates) != 1:
        raise FileNotFoundError(
            f"Expected exactly one 500M step-100 checkpoint in {INCOMING}, found {candidates}"
        )
    path = candidates[0]
    payload = torch.load(path, map_location="cpu", weights_only=False)
    if not isinstance(payload, dict) or int(payload.get("step", -1)) != EXPECTED_START_STEP:
        raise ValueError("Recovered checkpoint is not the exact step-100 student")
    if int(payload.get("parameter_count", -1)) != EXPECTED_PARAMETERS:
        raise ValueError(f"Checkpoint parameter count mismatch: {payload.get('parameter_count')}")
    config_data = payload.get("model_config")
    if not isinstance(config_data, dict):
        raise ValueError("500M checkpoint does not include model_config")
    config = ModelConfig(**config_data)
    model = RoninLM(config)
    model.load_state_dict(payload["model"], strict=True)
    if model.parameter_count != EXPECTED_PARAMETERS:
        raise AssertionError(f"Expected {EXPECTED_PARAMETERS} parameters, got {model.parameter_count}")
    del model
    gc.collect()
    payload["_path"] = str(path)
    payload["_sha256"] = sha256_file(path)
    return payload, config


@torch.inference_mode()
def evaluate_checkpoint(
    checkpoint_path: Path,
    rows: list[dict],
    all_rows_hash: str,
    base_config: ModelConfig,
    label: str,
) -> dict:
    """Evaluate all 64 identical MMLU-Pro validation items without truncation."""
    payload = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    config_data = payload.get("model_config")
    config = ModelConfig(**config_data)
    eval_config = replace(config, context_length=EVAL_CONTEXT)
    model = RoninLM(eval_config)
    model.load_state_dict(payload["model"], strict=True)
    del payload
    model.eval()

    details = []
    skipped = []
    for row in rows:
        prompt = format_prompt(row).encode("utf-8")
        if len(prompt) > EVAL_CONTEXT:
            skipped.append({"id": row["id"], "prompt_bytes": len(prompt)})
            continue
        input_ids = torch.tensor(list(prompt), dtype=torch.long).unsqueeze(0)
        last = torch.tensor([input_ids.shape[1] - 1], dtype=torch.long)
        logits = model.forward_last_logits(input_ids, last)
        scores = F.log_softmax(logits.float(), dim=-1)[0, [ord(c) for c in LABELS[:len(row["options"])]]]
        predicted = int(torch.argmax(scores).item())
        details.append({
            "id": row["id"],
            "category": row["category"],
            "options": len(row["options"]),
            "prompt_bytes": len(prompt),
            "correct_index": row["correct_index"],
            "predicted_index": predicted,
            "correct": predicted == row["correct_index"],
            "candidate_log_probabilities": [float(value) for value in scores.tolist()],
        })
        del input_ids, logits, scores

    del model
    gc.collect()
    if skipped or len(details) != EVAL_LIMIT:
        raise RuntimeError(
            f"{label}: paired evaluation coverage failed; evaluated={len(details)}, skipped={len(skipped)}"
        )

    grouped = defaultdict(list)
    for item in details:
        grouped[item["category"]].append(item)
    correct = sum(item["correct"] for item in details)
    return {
        "label": label,
        "benchmark": "MMLU-Pro",
        "dataset_revision": DATASET_REVISION,
        "dataset_split": "validation",
        "sampling": "same deterministic stratified 64-item sample, seed=2026",
        "dataset_sha256": all_rows_hash,
        "selected_items": EVAL_LIMIT,
        "evaluated_items": len(details),
        "skipped_items": len(skipped),
        "coverage": len(details) / EVAL_LIMIT,
        "checkpoint_sha256": sha256_file(checkpoint_path),
        "checkpoint_step": int(torch.load(checkpoint_path, map_location="cpu", weights_only=True).get("step", 0)),
        "model_parameters": EXPECTED_PARAMETERS,
        "trained_context_length": base_config.context_length,
        "evaluation_context_length": EVAL_CONTEXT,
        "context_note": "Evaluation context is extended beyond the 128-byte training context to avoid truncating benchmark prompts; this is not evidence of long-context training.",
        "overall": {
            "correct": correct,
            "total": len(details),
            "accuracy": correct / len(details),
        },
        "by_domain": {
            category: {
                "correct": sum(item["correct"] for item in items),
                "total": len(items),
                "accuracy": sum(item["correct"] for item in items) / len(items),
            }
            for category, items in sorted(grouped.items())
        },
        "question_ids": [item["id"] for item in details],
        "details": details,
        "official_score_comparable": False,
        "limitations": [
            "RONIN zero-shot next-byte option scoring; not the official MMLU-Pro chain-of-thought protocol.",
            "The 64-item validation sample is a screening measurement, not a full benchmark certification.",
            "The 50,000 Drosophila rows are procedural train candidates, not independently validated gold data.",
        ],
    }


def main() -> None:
    torch.set_num_threads(int(os.environ.get("OMP_NUM_THREADS", "4")))
    torch.set_num_interop_threads(1)
    OUT.mkdir(parents=True, exist_ok=True)

    corpus = build_drosophila_corpus()
    checkpoint_payload, model_config = load_student_checkpoint()
    checkpoint_path = Path(checkpoint_payload["_path"])
    checkpoint_sha = checkpoint_payload["_sha256"]
    del checkpoint_payload
    gc.collect()

    # The exact same 64 validation questions are scored before and after.
    all_rows = load_external_dataset(DATASET_REVISION, split="validation")
    rows = select_stratified(all_rows, EVAL_LIMIT, seed=EVAL_SEED)
    holdout_hash = rows_sha256(all_rows)
    before = evaluate_checkpoint(
        checkpoint_path, rows, holdout_hash, model_config, "before_drosophila_training"
    )
    write_json(OUT / "holdout-before.json", before)

    # Continue from the verified 500M/100-step weights. Optimizer state is
    # intentionally reinitialized because the source artifact is weights-only.
    source = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    model = RoninLM(model_config)
    model.load_state_dict(source["model"], strict=True)
    del source
    gc.collect()

    tokenizer = ByteTokenizer()
    tokens = encode_text_file(OUT / "drosophila-50k-train.txt", tokenizer)
    batches = NextTokenBatches(
        tokens,
        batch_size=1,
        sequence_length=model_config.context_length,
        seed=20261106,
    )
    training_config = TrainingConfig(
        batch_size=1,
        gradient_accumulation_steps=1,
        learning_rate=1.0e-5,
        min_learning_rate=1.0e-6,
        weight_decay=0.01,
        warmup_steps=25,
        max_steps=ADDITIONAL_STEPS,
        grad_clip_norm=1.0,
        seed=20261106,
        precision="fp32",
        checkpoint_every=ADDITIONAL_STEPS,
    )
    training_config.validate()
    checkpoint_dir = OUT / "temporary-full-checkpoints"
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
    if len(losses) != ADDITIONAL_STEPS:
        raise AssertionError(f"Expected {ADDITIONAL_STEPS} optimizer steps, got {len(losses)}")

    final_checkpoint = OUT / "student-500m-drosophila-step-00000600.pt"
    torch.save(
        {
            "model": model.state_dict(),
            "model_config": model_config.__dict__,
            "step": EXPECTED_START_STEP + ADDITIONAL_STEPS,
            "parameter_count": model.parameter_count,
            "seed": 20261106,
            "initial_checkpoint_sha256": checkpoint_sha,
            "training_steps_this_cycle": ADDITIONAL_STEPS,
            "training_corpus_sha256": corpus["text_sha256"],
            "tutor_used": False,
            "training_sources": ["HERETIC-RONIN Drosophila 01301-51300 only"],
            "optimizer_state_included": False,
        },
        final_checkpoint,
    )
    if model.parameter_count != EXPECTED_PARAMETERS:
        raise AssertionError("Parameter count changed during training")
    del model, tokens, batches
    gc.collect()

    # The large optimizer checkpoint is not part of the published artifact.
    for path in checkpoint_dir.glob("*"):
        path.unlink()
    checkpoint_dir.rmdir()

    after = evaluate_checkpoint(
        final_checkpoint, rows, holdout_hash, model_config, "after_500_drosophila_steps"
    )
    if before["question_ids"] != after["question_ids"]:
        raise AssertionError("Before/after holdout question IDs differ")
    if before["dataset_sha256"] != after["dataset_sha256"]:
        raise AssertionError("Before/after holdout dataset hashes differ")
    write_json(OUT / "holdout-after.json", after)

    report = {
        "experiment": "heretic-500m-drosophila-50k-no-tutor-500-steps-v1",
        "base_run_id": ARTIFACT_RUN_ID,
        "base_artifact": ARTIFACT_NAME,
        "base_checkpoint_step": EXPECTED_START_STEP,
        "base_checkpoint_sha256": checkpoint_sha,
        "student_parameters": EXPECTED_PARAMETERS,
        "additional_training_steps": ADDITIONAL_STEPS,
        "resulting_step": EXPECTED_START_STEP + ADDITIONAL_STEPS,
        "tutor_used": False,
        "training_sources": ["HERETIC-RONIN Drosophila 01301-51300 only"],
        "training_corpus": corpus,
        "training_metrics": {
            "steps_completed": len(losses),
            "initial_loss": losses[0],
            "final_loss": losses[-1],
            "mean_first_25": sum(losses[:25]) / 25,
            "mean_last_25": sum(losses[-25:]) / 25,
            "checkpoint": str(final_checkpoint),
            "checkpoint_bytes": final_checkpoint.stat().st_size,
            "checkpoint_sha256": sha256_file(final_checkpoint),
        },
        "paired_holdout": {
            "dataset": "TIGER-Lab/MMLU-Pro",
            "revision": DATASET_REVISION,
            "split": "validation",
            "items": EVAL_LIMIT,
            "seed": EVAL_SEED,
            "same_question_ids": True,
            "before": before["overall"],
            "after": after["overall"],
            "delta_correct": after["overall"]["correct"] - before["overall"]["correct"],
            "delta_percentage_points": (
                after["overall"]["accuracy"] - before["overall"]["accuracy"]
            ) * 100.0,
            "by_domain_before": before["by_domain"],
            "by_domain_after": after["by_domain"],
            "holdout_sha256": holdout_hash,
        },
        "interpretation": (
            "No-tutor continuation experiment. Only the new 50,000-row Drosophila train_candidate "
            "shards were used for these 500 optimizer steps. The original 100-step checkpoint "
            "was initialized and trained earlier on a separate admitted corpus; that history is "
            "not attributed to this Drosophila-only cycle."
        ),
        "automatic_promotion": False,
    }
    write_json(OUT / "experiment-report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
