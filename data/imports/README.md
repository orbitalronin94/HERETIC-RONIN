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

The initial source-scoped import was correctly held while global G-0 was FAIL. That status was superseded for the exact combined corpus by global audit [42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447), which included the train-only RONIN-IA material plus the explicitly curated Cosmopedia v0.1 slice. It examined 261,039 documents, excluded 68 duplicate endpoints, found zero exact matches against 120 synthetic diagnostic questions and reported `training_authorized=true`. This grants internal experimental train-only use to that exact audited subset; it does not authorize any other candidates, redistribution, model promotion or use of validation/test/holdout. The verified source-scoped total is **286,464 documents** (270,244 CoVoST + 7,103 ScienceVerse + 8,498 Mathlib4 + 608 literature + 2 NASA + 9 Papers).

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

## Estado posterior de auditoría global — 2026-11-07

- Auditoría combinada: [run 42362365447](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42362365447).
- Corpus examinado: 261.039 documentos; 68 extremos duplicados excluidos; 260.971 documentos dentro del subconjunto autorizado.
- Cosmopedia v0.1 `auto_math_text/train`: 4.734 filas, 22.927.899 bytes, SHA-256 `f474a3d8bd7a18ab7cac222ae1f2906c52bdaa346a27ca0df728039ac1438f9a`; admitida solo para next-token pretraining experimental.
- Total admitido contabilizado: 703.593.871 bytes (base RONIN-IA 680.665.972 + Cosmopedia 22.927.899).
- El piloto [42358300901](https://github.com/orbitalronin94/HERETIC-RONIN/actions/runs/42358300901) comenzó antes de esta admisión y no consume Cosmopedia.
- Los derechos de Papers siguen limitados al entrenamiento interno; esta autorización no es permiso de redistribución.
