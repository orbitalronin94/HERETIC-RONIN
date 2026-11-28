#!/usr/bin/env python3
"""Train a fresh HERETIC-RONIN model from random initialization on train-only tokens."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import time
from pathlib import Path

import numpy as np
import torch

from heretic_ronin import HereticConfig, HereticRoninLM


class FactoredAdafactor:
    """CPU-friendly factored second moments; no full-size Adam moment tensors."""
    def __init__(self, parameters, lr=8e-5, beta2_decay=-0.8,
                 eps=1e-30, weight_decay=0.01, clip_threshold=1.0):
        self.parameters = list(parameters)
        self.lr = lr
        self.beta2_decay = beta2_decay
        self.eps = eps
        self.weight_decay = weight_decay
        self.clip_threshold = clip_threshold
        self.state = {}
        self.step_number = 0

    @torch.no_grad()
    def step(self):
        self.step_number += 1
        beta2 = 1.0 - self.step_number ** self.beta2_decay
        for parameter in self.parameters:
            grad = parameter.grad
            if grad is None:
                continue
            state = self.state.setdefault(id(parameter), {})
            if parameter.ndim >= 2:
                if "row" not in state:
                    state["row"] = torch.zeros(
                        (parameter.shape[0],) + (1,) * (parameter.ndim - 1),
                        dtype=parameter.dtype, device=parameter.device)
                    state["col"] = torch.zeros(
                        (1,) + tuple(parameter.shape[1:]),
                        dtype=parameter.dtype, device=parameter.device)
                square = grad.square()
                dimensions = tuple(range(1, square.ndim))
                row_mean = square.mean(dim=dimensions, keepdim=True)
                col_mean = square.mean(dim=0, keepdim=True)
                state["row"].mul_(beta2).add_(row_mean, alpha=1.0-beta2)
                state["col"].mul_(beta2).add_(col_mean, alpha=1.0-beta2)
                row_level = state["row"].mean().clamp_min(self.eps)
                variance = state["row"] * state["col"] / row_level
            else:
                if "variance" not in state:
                    state["variance"] = torch.zeros_like(parameter)
                state["variance"].mul_(beta2).addcmul_(
                    grad, grad, value=1.0-beta2)
                variance = state["variance"]
            update = grad * torch.rsqrt(variance + self.eps)
            rms = update.square().mean().sqrt().clamp_min(self.eps)
            update.div_(torch.clamp(rms / self.clip_threshold, min=1.0))
            if self.weight_decay:
                parameter.mul_(1.0 - self.lr * self.weight_decay)
            parameter.add_(update, alpha=-self.lr)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def sample_batch(data: np.memmap, rng: np.random.Generator,
                 batch_size: int, sequence_length: int) -> torch.Tensor:
    if len(data) <= sequence_length + 1:
        raise RuntimeError("Token corpus is shorter than one training sequence")
    rows = []
    for _ in range(batch_size):
        start = int(rng.integers(0, len(data) - sequence_length - 1))
        rows.append(np.asarray(
            data[start:start + sequence_length + 1], dtype=np.int64))
    return torch.from_numpy(np.stack(rows)).long()


@torch.no_grad()
def evaluate(model, data, seed: int, batches: int, sequence_length: int) -> float:
    model.eval()
    rng = np.random.default_rng(seed)
    losses = []
    for _ in range(batches):
        batch = sample_batch(data, rng, 1, sequence_length)
        _, loss = model(batch, labels=batch)
        if loss is None or not torch.isfinite(loss):
            raise FloatingPointError("Non-finite evaluation loss")
        losses.append(float(loss))
    model.train()
    return float(np.mean(losses))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--steps", type=int, default=100)
    parser.add_argument("--threads", type=int, default=4)
    parser.add_argument("--sequence-length", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--seed", type=int, default=20261110)
    parser.add_argument("--config", default=None)
    args = parser.parse_args()
    if args.steps < 1 or args.sequence_length > 512:
        parser.error("steps must be positive and sequence length must be <= 512")
    torch.set_num_threads(args.threads)
    torch.set_num_interop_threads(2)
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    random.seed(args.seed)

    data_dir = Path(args.data_dir)
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    train_path = data_dir / "train.bin"
    manifest_path = data_dir / "encoding-manifest.json"
    tokenizer_path = data_dir / "tokenizer.json"
    for path in (train_path, manifest_path, tokenizer_path):
        if not path.is_file() or path.stat().st_size == 0:
            raise SystemExit(f"Required fresh-training input missing: {path}")
    corpus_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if corpus_manifest.get("schema") != "heretic-tokenized-corpus-v1":
        raise SystemExit("Unexpected tokenized corpus manifest")
    if corpus_manifest.get("tokenizer_sha256") != sha256(tokenizer_path):
        raise SystemExit("Tokenizer SHA-256 does not match encoding manifest")
    train_data = np.memmap(train_path, mode="r", dtype="<u2")
    if len(train_data) < 1000:
        raise SystemExit("Train token stream is too small")

    if args.config:
        config_data = json.loads(Path(args.config).read_text(encoding="utf-8"))
        config = HereticConfig(**config_data)
    else:
        config = HereticConfig()
    model = HereticRoninLM(config).cpu()
    model.assert_fully_trainable()
    total = model.parameter_count(trainable_only=False)
    trainable = model.parameter_count(trainable_only=True)
    if total != trainable:
        raise SystemExit(f"Frozen parameter audit failed: {trainable}/{total}")
    if config == HereticConfig() and total != 500_141_056:
        raise SystemExit(f"500M architecture audit failed: {total} != 500141056")
    config.save(out / "config.json")

    optimizer = FactoredAdafactor(model.parameters(), lr=8e-5)
    rng = np.random.default_rng(args.seed + 1)
    baseline = None
    losses = []
    started = time.perf_counter()
    model.train()
    for step in range(1, args.steps + 1):
        progress = step / args.steps
        optimizer.lr = 8e-5 * (0.2 + 0.8 * 0.5 * (1.0 + math.cos(math.pi * progress)))
        batch = sample_batch(train_data, rng, args.batch_size, args.sequence_length)
        for parameter in model.parameters():
            parameter.grad = None
        _, loss = model(batch, labels=batch)
        if loss is None or not torch.isfinite(loss):
            raise FloatingPointError(f"Non-finite training loss at step {step}")
        loss.backward()
        grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        if not torch.isfinite(grad_norm):
            raise FloatingPointError(f"Non-finite gradient norm at step {step}")
        optimizer.step()
        losses.append(float(loss.detach()))
        if step == 1 or step % 10 == 0 or step == args.steps:
            print(json.dumps({
                "event": "fresh_train_step", "step": step,
                "total_steps": args.steps, "loss": losses[-1],
                "lr": optimizer.lr,
                "elapsed_seconds": round(time.perf_counter() - started, 2),
            }), flush=True)

    checkpoint_path = out / f"heretic-ronin-fresh-step-{args.steps}.pt"
    torch.save({
        "model_state_dict": model.state_dict(),
        "model_config": config.__dict__,
        "parameter_count": total,
        "trainable_parameter_count": trainable,
        "all_parameters_trainable": True,
        "completed_steps": args.steps,
        "seed": args.seed,
        "initialization": "random_normal_std_0.02",
        "parent_checkpoint_sha256": None,
        "optimizer": "factored Adafactor",
        "optimizer_state_included": False,
        "tokenizer_sha256": sha256(tokenizer_path),
        "encoding_manifest_sha256": sha256(manifest_path),
    }, checkpoint_path)
    report = {
        "experiment": "HERETIC-RONIN-from-scratch",
        "initialization": "random; no inherited checkpoint or optimizer state",
        "steps": args.steps,
        "parameters": total,
        "trainable_parameters": trainable,
        "all_parameters_trainable": True,
        "architecture": config.__dict__,
        "seed": args.seed,
        "sequence_length": args.sequence_length,
        "batch_size": args.batch_size,
        "training_tokens": args.steps * args.sequence_length * args.batch_size,
        "mean_training_loss": float(np.mean(losses)),
        "first_10_mean_loss": float(np.mean(losses[:10])),
        "last_10_mean_loss": float(np.mean(losses[-10:])),
        "elapsed_seconds": round(time.perf_counter() - started, 2),
        "tokenizer_sha256": sha256(tokenizer_path),
        "encoding_manifest_sha256": sha256(manifest_path),
        "checkpoint": checkpoint_path.name,
        "checkpoint_sha256": sha256(checkpoint_path),
        "validation": "not measured in this first train-only pilot; holdout evaluation is a separate gate",
        "promotion": "NOT_ELIGIBLE; pilot only",
    }
    (out / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
