#!/usr/bin/env python3
"""Append one successful real-checkpoint inference to docs/REAL_INFERENCE_LOG.md."""
import json
import os
from pathlib import Path

payload = json.loads(Path(os.environ["INFERENCE_JSON"]).read_text(encoding="utf-8"))
run_id = os.environ["RUN_ID"]
run_url = os.environ["RUN_URL"]
target = Path("docs/REAL_INFERENCE_LOG.md")
text = target.read_text(encoding="utf-8")
marker = f"<!-- run:{run_id} -->"
if marker in text:
    print(f"Run {run_id} already archived; no change.")
    raise SystemExit(0)

prompt = str(payload.get("prompt", ""))
completion = str(payload.get("completion", ""))
if not prompt or not completion:
    raise SystemExit("Inference artifact lacks a prompt or completion; refusing to archive.")
step = payload.get("checkpoint_step", "unknown")
params = payload.get("parameter_count", "unknown")
generation = payload.get("generation", "unknown")
note = payload.get("note", "")
entry = f"""
{marker}
## Inferencia — run {run_id}

- Run: [{run_id}]({run_url})
- Checkpoint: step {step}
- Parámetros: {params}
- Decodificación: {generation}
- Nota: {note}

**Prompt**
\x60\x60\x60text
{prompt}
\x60\x60\x60

**Continuación literal**
\x60\x60\x60text
{completion}
\x60\x60\x60
"""
target.write_text(text.rstrip() + "\n\n" + entry.lstrip(), encoding="utf-8")
print(f"Archived real inference from run {run_id}.")
