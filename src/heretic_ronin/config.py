"""Auditable from-scratch HERETIC-RONIN model configuration."""
from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class HereticConfig:
    vocab_size: int = 32768
    context_length: int = 512
    n_layers: int = 37
    d_model: int = 1024
    n_heads: int = 16
    d_ff: int = 4096
    dropout: float = 0.0
    layer_norm_eps: float = 1e-5
    tie_embeddings: bool = True
    gradient_checkpointing: bool = True

    def validate(self) -> None:
        if self.d_model % self.n_heads:
            raise ValueError("d_model must be divisible by n_heads")
        if min(self.vocab_size, self.context_length, self.n_layers,
               self.d_model, self.n_heads, self.d_ff) <= 0:
            raise ValueError("model dimensions must be positive")
        if not 0.0 <= self.dropout < 1.0:
            raise ValueError("dropout must be in [0, 1)")
        if not self.tie_embeddings:
            raise ValueError("HERETIC-RONIN requires tied input/output embeddings")

    def save(self, path: str | Path) -> None:
        self.validate()
        Path(path).write_text(json.dumps(asdict(self), indent=2) + "\\n", encoding="utf-8")
