#!/usr/bin/env python3
"""HERETIC-500M continuation with 40-microbatch gradient accumulation.

The transition checkpoint is a global micro-step checkpoint from the original
batch-2 run. Its model weights are retained; the old optimizer is deliberately
reset once at the transition because batch size, LR schedule and Adam moments
are changing. All subsequent chunks resume optimizer, scheduler and RNG state.
"""
from __future__ import annotations
import argparse, json, random, time
from pathlib import Path

import numpy as np
import torch

from ronin.config import ModelConfig
from ronin.models.transformer import RoninLM
from heretic_train_real_corpus_250k import build_corpus, evaluate, sha256

CONTEXT = 128
MICRO_BATCH = 2
ACCUM_STEPS = 40
TOKENS_PER_MICRO_STEP = CONTEXT * MICRO_BATCH
TOKENS_PER_OPTIMIZER_STEP = TOKENS_PER_MICRO_STEP * ACCUM_STEPS
TARGET_MICRO_STEP = 250_000
SEED = 20261106

# Important: the current 250k script uses LR=1e-5, not 6e-4.
# sqrt(40) scaling therefore gives 6.3246e-5, not 3.8e-3.
BASE_LR = 1e-5
LR = BASE_LR * (ACCUM_STEPS ** 0.5)
WARMUP_OPTIMIZER_STEPS = 200
BETAS = (0.9, 0.999)
WEIGHT_DECAY = 0.01
EPS = 1e-8
OUT = Path("out")


def scheduler_lambda(step: int) -> float:
    return min(1.0, (step + 1) / WARMUP_OPTIMIZER_STEPS)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-micro-step", type=int, required=True)
    parser.add_argument("--micro-steps", type=int, required=True)
    parser.add_argument("--resume-accum", action="store_true")
    args = parser.parse_args()

    if args.micro_steps <= 0 or args.micro_steps % ACCUM_STEPS:
        raise RuntimeError(f"micro-steps must be positive and divisible by {ACCUM_STEPS}")
    if args.start_micro_step + args.micro_steps > TARGET_MICRO_STEP:
        raise RuntimeError("Chunk exceeds global target micro-step")
    if args.start_micro_step < 2600:
        raise RuntimeError("Accumulation transition is authorized only from micro-step 2600 onward")

    OUT.mkdir(exist_ok=True)
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)

    corpus, corpus_info = build_corpus(
        Path("incoming/ronin-ia-train.zip"),
        Path("incoming/GLOBAL-CORPUS-AUDIT.json"),
    )
    checkpoint = torch.load("incoming/checkpoint.pt", map_location="cpu", weights_only=False)
    if int(checkpoint.get("step", -1)) != args.start_micro_step:
        raise RuntimeError(
            f"Checkpoint micro-step {checkpoint.get('step')} != requested {args.start_micro_step}"
        )

    config = ModelConfig(**checkpoint["model_config"])
    model = RoninLM(config)
    model.load_state_dict(checkpoint["model"], strict=True)
    if model.parameter_count != 500102144:
        raise RuntimeError(f"Unexpected parameter count {model.parameter_count}")

    seed = int(checkpoint.get("seed", SEED))
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LR,
        betas=BETAS,
        weight_decay=WEIGHT_DECAY,
        eps=EPS,
    )
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, scheduler_lambda)

    if args.resume_accum:
        if int(checkpoint.get("accum_steps", -1)) != ACCUM_STEPS:
            raise RuntimeError("Resume checkpoint does not use ACCUM_STEPS=40")
        if "optimizer_state_dict" not in checkpoint or "scheduler_state_dict" not in checkpoint:
            raise RuntimeError("Accumulation resume checkpoint is missing optimizer/scheduler state")
        optimizer.load_state_dict(checkpoint["optimizer_state_dict"])
        scheduler.load_state_dict(checkpoint["scheduler_state_dict"])
        optimizer_step = int(checkpoint["optimizer_step"])
        rng = random.Random()
        rng.setstate(checkpoint["python_rng_state"])
        torch.set_rng_state(checkpoint["torch_rng_state"])
        np.random.set_state(checkpoint["numpy_rng_state"])
        before = json.loads(Path("incoming/holdout-before.json").read_text())
        previous_losses = checkpoint.get("loss_tail", [])
    else:
        # Deliberate one-time optimizer reset at the batch-regime transition.
        # The exact 500M model weights are carried forward unchanged.
        optimizer_step = 0
        rng = random.Random(seed + args.start_micro_step)
        torch.manual_seed(seed + args.start_micro_step)
        np.random.seed((seed + args.start_micro_step) % (2**32 - 1))
        before = evaluate(model)
        Path("out/holdout-before.json").write_text(
            json.dumps(before, ensure_ascii=False, indent=2) + "\n"
        )
        previous_losses = []

    names = list(corpus)
    weights = [len(corpus[name]) ** 0.5 for name in names]
    model.train()
    optimizer.zero_grad(set_to_none=True)

    losses = []
    grad_norms = []
    started = time.perf_counter()
    end_micro_step = args.start_micro_step + args.micro_steps

    for local in range(args.micro_steps):
        xs, ys = [], []
        source = rng.choices(names, weights=weights, k=1)[0]
        buffer = corpus[source]
        for _ in range(MICRO_BATCH):
            start = rng.randrange(0, len(buffer) - CONTEXT - 1)
            sequence = buffer[start : start + CONTEXT + 1].astype(np.int64, copy=False)
            xs.append(sequence[:-1])
            ys.append(sequence[1:])

        x = torch.from_numpy(np.stack(xs))
        y = torch.from_numpy(np.stack(ys))
        _, loss = model(x, y)
        if loss is None or not torch.isfinite(loss):
            raise FloatingPointError(
                f"non-finite loss at micro-step {args.start_micro_step + local + 1}"
            )

        # Accumulate the MEAN gradient across 40 micro-batches.
        (loss / ACCUM_STEPS).backward()
        losses.append(float(loss.detach()))

        if (local + 1) % ACCUM_STEPS == 0:
            # Clip only after all 40 micro-gradients have been accumulated.
            grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            if not torch.isfinite(grad_norm):
                raise FloatingPointError(
                    f"non-finite accumulated gradient at micro-step {args.start_micro_step + local + 1}"
                )
            grad_norms.append(float(grad_norm.detach()))
            optimizer.step()
            optimizer.zero_grad(set_to_none=True)
            scheduler.step()
            optimizer_step += 1

        if (local + 1) % 100 == 0:
            global_micro = args.start_micro_step + local + 1
            print(
                f"micro_step={global_micro} optimizer_step={optimizer_step} "
                f"loss={losses[-1]:.6f} grad_norm="
                f"{grad_norms[-1] if grad_norms else float('nan'):.4f} "
                f"lr={optimizer.param_groups[0]['lr']:.8g} source={source}",
                flush=True,
            )

    if (args.micro_steps % ACCUM_STEPS) != 0:
        raise RuntimeError("Refusing to checkpoint a partial gradient accumulation window")

    after = evaluate(model)
    Path("out/holdout-after.json").write_text(
        json.dumps(after, ensure_ascii=False, indent=2) + "\n"
    )
    progress = {
        "start_micro_step": args.start_micro_step,
        "end_micro_step": end_micro_step,
        "micro_steps_this_chunk": args.micro_steps,
        "optimizer_steps_this_chunk": args.micro_steps // ACCUM_STEPS,
        "optimizer_step_total": optimizer_step,
        "accum_steps": ACCUM_STEPS,
        "micro_batch_sequences": MICRO_BATCH,
        "context_tokens": CONTEXT,
        "tokens_per_micro_step": TOKENS_PER_MICRO_STEP,
        "tokens_per_optimizer_step": TOKENS_PER_OPTIMIZER_STEP,
        "tokens_this_chunk": args.micro_steps * TOKENS_PER_MICRO_STEP,
        "tokens_since_transition": (end_micro_step - 2600) * TOKENS_PER_MICRO_STEP,
        "base_lr_from_actual_current_script": BASE_LR,
        "peak_lr": LR,
        "warmup_optimizer_steps": WARMUP_OPTIMIZER_STEPS,
        "betas": BETAS,
        "weight_decay": WEIGHT_DECAY,
        "mean_microbatch_loss": float(np.mean(losses)),
        "first_100_mean_loss": float(np.mean(losses[:100])),
        "last_100_mean_loss": float(np.mean(losses[-100:])),
        "grad_norm_p50": float(np.percentile(grad_norms, 50)),
        "grad_norm_p95": float(np.percentile(grad_norms, 95)),
        "grad_norm_max": float(np.max(grad_norms)),
        "holdout_before": {
            "correct": before["correct"],
            "total": before["total"],
            "accuracy": before["accuracy"],
            "by_domain": before["by_domain"],
        },
        "holdout_after": {
            "correct": after["correct"],
            "total": after["total"],
            "accuracy": after["accuracy"],
            "by_domain": after["by_domain"],
        },
        "holdout_delta_percentage_points": (after["accuracy"] - before["accuracy"]) * 100,
        "corpus": corpus_info,
        "elapsed_seconds": time.perf_counter() - started,
        "optimizer_reset_at_transition": not args.resume_accum,
    }
    Path("out/progress.json").write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n"
    )

    checkpoint_out = {
        "model": model.state_dict(),
        "model_config": config.__dict__,
        "step": end_micro_step,
        "micro_step": end_micro_step,
        "optimizer_step": optimizer_step,
        "parameter_count": model.parameter_count,
        "seed": seed,
        "accum_steps": ACCUM_STEPS,
        "micro_batch_sequences": MICRO_BATCH,
        "context_tokens": CONTEXT,
        "optimizer": "AdamW",
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict(),
        "optimizer_state_included": True,
        "scheduler_state_included": True,
        "python_rng_state": rng.getstate(),
        "torch_rng_state": torch.get_rng_state(),
        "numpy_rng_state": np.random.get_state(),
        "base_lr": BASE_LR,
        "peak_lr": LR,
        "warmup_optimizer_steps": WARMUP_OPTIMIZER_STEPS,
        "betas": BETAS,
        "weight_decay": WEIGHT_DECAY,
        "corpus_manifest": corpus_info,
        "loss_tail": (previous_losses + losses)[-1000:],
        "training_scope": "real source-scoped RONIN-IA train artifacts only",
        "transition": "step-2600 weights; optimizer reset once for accum40 regime",
    }
    torch.save(checkpoint_out, "out/checkpoint.pt")
    progress["checkpoint_sha256"] = sha256("out/checkpoint.pt")
    Path("out/progress.json").write_text(
        json.dumps(progress, ensure_ascii=False, indent=2) + "\n"
    )

    report = {
        "experiment": "HERETIC-500M-real-corpus-accum40",
        "start_micro_step": args.start_micro_step,
        "end_micro_step": end_micro_step,
        "optimizer_step_total": optimizer_step,
        "parameters": model.parameter_count,
        "accum_steps": ACCUM_STEPS,
        "tokens_per_optimizer_step": TOKENS_PER_OPTIMIZER_STEP,
        "holdout_before": {k: v for k, v in before.items() if k != "details"},
        "holdout_after": {k: v for k, v in after.items() if k != "details"},
        "accuracy_delta_percentage_points": (after["accuracy"] - before["accuracy"]) * 100,
        "promotion": "NOT_AUTOMATIC; inspect per-domain results, loss/token and all 120 predictions",
    }
    Path("out/chunk-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(progress, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
