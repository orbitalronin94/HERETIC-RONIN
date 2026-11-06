#!/usr/bin/env python3
"""Numerical regression test for 40-way gradient accumulation."""
import copy
import torch
import torch.nn.functional as F

from heretic_train_accum40 import (
    ACCUM_STEPS, LR, TOKENS_PER_OPTIMIZER_STEP, scheduler_lambda
)

assert ACCUM_STEPS == 40
assert TOKENS_PER_OPTIMIZER_STEP == 10240
assert abs(LR - 1e-5 * (40 ** 0.5)) < 1e-12
assert scheduler_lambda(0) == 1 / 200
assert scheduler_lambda(199) == 1
assert scheduler_lambda(200) == 1

torch.manual_seed(1234)
micro_batches = [(torch.randn(2, 8), torch.randint(0, 5, (2,))) for _ in range(40)]
reference = torch.nn.Linear(8, 5)
accumulated = copy.deepcopy(reference)

# Reference: one large batch of 80 examples.
all_x = torch.cat([x for x, _ in micro_batches], dim=0)
all_y = torch.cat([y for _, y in micro_batches], dim=0)
reference_loss = F.cross_entropy(reference(all_x), all_y)
reference_loss.backward()

# Candidate: 40 micro-batches; mean loss scaled before backward.
optimizer = torch.optim.SGD(accumulated.parameters(), lr=0.0)
optimizer.zero_grad(set_to_none=True)
micro_losses = []
for x, y in micro_batches:
    loss = F.cross_entropy(accumulated(x), y)
    micro_losses.append(float(loss.detach()))
    (loss / ACCUM_STEPS).backward()

for (name_ref, p_ref), (name_acc, p_acc) in zip(
    reference.named_parameters(), accumulated.named_parameters()
):
    assert name_ref == name_acc
    error = (p_ref.grad - p_acc.grad).abs().max().item()
    assert error < 1e-7, f"{name_ref}: accumulated gradient mismatch {error}"

# Clipping once after accumulation must preserve a finite global norm.
norm = torch.nn.utils.clip_grad_norm_(accumulated.parameters(), 1.0)
assert torch.isfinite(norm)
print({
    "accum_steps": ACCUM_STEPS,
    "tokens_per_optimizer_step": TOKENS_PER_OPTIMIZER_STEP,
    "reference_loss": float(reference_loss.detach()),
    "mean_micro_loss": sum(micro_losses) / len(micro_losses),
    "preclip_grad_norm": float(norm),
    "gradient_equivalence": "PASS",
})
