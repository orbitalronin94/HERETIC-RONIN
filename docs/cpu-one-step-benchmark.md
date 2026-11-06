# HERETIC CPU one-step benchmark

This workflow is an isolated experiment. It never writes to the production training
checkpoint, never dispatches the continuation workflow, and never promotes a model.

## Comparison contract

- Exact 500,102,144-parameter checkpoint at global micro-step 2600.
- Same signed corpus audit and same immutable train-only artifact for the baseline.
- One optimizer update per run: 40 micro-batches × 2 sequences × 128 tokens = 10,240 tokens.
- The baseline creates one deterministic batch plan. Every candidate reuses those exact
  tensors and starts from a fresh load of the same checkpoint.
- Candidate jobs are limited to two concurrent CPU runners to reduce noisy contention.
- Reports include wall/CPU time, effective tokens/s, data preparation time, peak RSS,
  loss, gradient norm and a parameter fingerprint.

## Candidate matrix

| Candidate | What changes | Guard |
|---|---|---|
| threads-1 / threads-2 / threads-8 | intra-op CPU thread count | same inputs and FP32 path |
| cpu-affinity | restrict process to a subset of allowed CPUs | runner must expose affinity |
| mkldnn-disabled | disable oneDNN/MKLDNN as a control against the default backend | default backend remains baseline |
| bf16-autocast | CPU BF16 autocast | diagnostic only; never auto-eligible |
| torch-compile | CPU Inductor compilation | compilation cost included in the measured step; diagnostic only |
| adamw-foreach | AdamW foreach implementation | loss, gradient norm and parameter fingerprint compared |
| mmap-batches | memory-mapped serialized batch plan | identical token tensors |
| sharded-prefetch | bounded shard read before the optimizer update | shard preparation included in end-to-end time |
| packed-window-cache | stack fixed-length windows without crossing document boundaries | same token tensors |
| inference-mode-eval | measure holdout evaluation path | audit only; current predictor already uses inference mode |

## CI / DevOps

The baseline job is the cold-install control; candidate jobs enable setup-python's pip
cache. The workflow records the same one-step training measurements in both. Hosted
GitHub runners are ephemeral, so persistent machine/environment reuse is not treated as
a valid optimization here; jobs reuse their environment only within their own lifetime.

## Decision policy

A candidate is only eligible for manual review if end-to-end time improves and mean loss,
gradient norm and the parameter fingerprint stay within the configured numerical
tolerances. BF16, torch.compile and inference-mode audit are diagnostic-only. No candidate
is automatically merged into the production training workflow. A passing one-step result
must be repeated over a longer segment before adoption.
