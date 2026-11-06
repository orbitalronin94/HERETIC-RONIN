#!/usr/bin/env python3
"""Run one real greedy inference from the exact HERETIC 500M step-600 checkpoint."""
from __future__ import annotations
import gc, json, os
from pathlib import Path
import torch
from ronin.config import ModelConfig
from ronin.models.transformer import RoninLM
from ronin.tokenizer.byte import ByteTokenizer

CHECKPOINT = Path("incoming/student-500m-multidomain-distilled.pt")
PROMPT = os.environ.get(
    "HERETIC_PROMPT",
    "Explica por qué la división por cero no está definida."
)
MAX_NEW = int(os.environ.get("HERETIC_MAX_NEW_TOKENS", "72"))

def main() -> None:
    torch.set_num_threads(4)
    torch.set_num_interop_threads(1)
    print("Loading exact checkpoint:", CHECKPOINT, flush=True)
    checkpoint = torch.load(CHECKPOINT, map_location="cpu", weights_only=False, mmap=True)
    config_data = checkpoint.get("model_config")
    state = checkpoint.get("model")
    if not isinstance(config_data, dict) or not isinstance(state, dict):
        raise RuntimeError("Checkpoint lacks model_config or model state")
    step = int(checkpoint.get("step", -1))
    params = int(checkpoint.get("parameter_count", -1))
    config = ModelConfig(**config_data)
    model = RoninLM(config)
    model.load_state_dict(state, strict=True, assign=True)
    if model.parameter_count != 500_102_144 or params != 500_102_144:
        raise RuntimeError(f"Unexpected parameter count: model={model.parameter_count}, metadata={params}")
    if step != 600:
        raise RuntimeError(f"Expected exact step-600 checkpoint, got step={step}")
    del state, checkpoint
    gc.collect()
    model.eval()

    tokenizer = ByteTokenizer()
    prompt_ids = tokenizer.encode("Q: " + PROMPT + "\nA:")
    if len(prompt_ids) >= config.context_length:
        raise RuntimeError(f"Prompt too long for {config.context_length}-byte context")
    generated: list[int] = []
    with torch.inference_mode():
        for _ in range(MAX_NEW):
            context = (prompt_ids + generated)[-config.context_length:]
            input_ids = torch.tensor([context], dtype=torch.long)
            last = torch.tensor([len(context) - 1], dtype=torch.long)
            logits = model.forward_last_logits(input_ids, last)
            token = int(torch.argmax(logits[0]).item())
            if token in (10, 13):
                break
            generated.append(token)
    answer = tokenizer.decode(generated).strip()
    print("\n=== HERETIC REAL WEIGHT INFERENCE ===")
    print(json.dumps({
        "checkpoint": str(CHECKPOINT),
        "global_step": step,
        "parameters": model.parameter_count,
        "architecture": {
            "layers": config.n_layers,
            "width": config.d_model,
            "heads": config.n_heads,
            "context_bytes": config.context_length,
        },
        "decoding": "greedy_argmax",
        "prompt": PROMPT,
        "answer": answer,
        "warning": "Actual model output from checkpoint weights; step-600 experimental checkpoint, not the current later 250k run."
    }, ensure_ascii=False, indent=2), flush=True)

if __name__ == "__main__":
    main()
