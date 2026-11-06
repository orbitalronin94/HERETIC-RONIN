# RONIN-IA import into HERETIC-RONIN

This directory documents the reproducible source-scoped import pipeline. Bulk corpus payloads are stored as immutable GitHub Actions artifacts rather than committed to Git history.

## Current scope

The importer stages only explicitly scoped `train` payloads. The current source inventory in RONIN-IA's README says 286,468 train documents, but reconciliation against the exact downloadable artifacts gives **286,464**: NASA's latest file-reviewed artifact has 2 train documents and 4 held mismatches, not 6 train. This discrepancy is recorded rather than silently counted. The importer now fetches the exact Mathlib4 artifact (run `42026633643`, SHA-256 checked) instead of omitting its 8,498 train files.

The source breakdown is:

- CoVoST 2 translation-only: 270,244 segments, CC0-1.0, train gzip SHA-256 verified.
- ScienceVerse: 7,103 train documents from the audited train-only artifact; 262 held records excluded.
- Spanish literature: 608 train documents; validation and test files excluded.
- NASA NTRS file-reviewed: 2 individually reviewed train documents; 4 review/payload mismatches excluded. Artifact: run `42028138060`.
- RONIN-authored Papers: 9 Markdown files at the pinned Papers revision, README excluded; owner authorization is limited to internal RONIN training.

Mathlib4: 8,498 train documents under Apache-2.0, imported from the exact audited train-only artifact `ronin-admitted-mathlib4-v1` (run `42026633643`). Both `train.txt` and `documents.train.jsonl.gz` are SHA-256 verified; validation/test remain excluded.

## Safety boundary

The current RONIN-IA manifests report global G-0 as FAIL, with global near-duplicate and benchmark/holdout contamination checks pending. Therefore the bundle remains `staged_train_not_active_training`. Source-scoped eligibility is not a global contamination clearance. The importer deliberately excludes validation, test and held partitions and does not authorize model training or model promotion. The verified source-scoped total is **286,464 documents** (270,244 CoVoST + 7,103 ScienceVerse + 8,498 Mathlib4 + 608 literature + 2 NASA + 9 Papers).

## Reproduction

- Workflow: [import-ronin-ia-train.yml](../../.github/workflows/import-ronin-ia-train.yml)
- Importer: [import_ronin_ia_train.py](../../scripts/import_ronin_ia_train.py)
- Source registry: [registry.json](../sources/registry.json)

Each run verifies SHA-256 values and publishes a 90-day artifact with `IMPORT-MANIFEST.json`. Bulk data is not committed to Git because that would inflate Git history and make future revisions difficult to manage.


## Primera materialización completa de train scoped

- Run HERETIC: [42283514919](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42283514919)
- Artefacto: `heretic-ronin-ia-train-staged-42283514919` (288.668.608 bytes; SHA-256 del ZIP: `8a1e6be6a02b97b24681f2d34909cf4562213e84d0b9824f4ebca64a279e9cef`).
- Resultado del manifiesto: `records_staged=286464`, `active_training_authorized=false`, `global_g0=FAIL`.
- Mathlib4 train se recuperó desde el artefacto de RONIN-IA run `42026633643`; el SHA-256 del texto es `7c82a4d1e0f3788d6038002b41ae1ead1bf6a16cbf4e332f59f015501325667c`.
- El bundle incluye únicamente train. No contiene validation, test ni holdout.
