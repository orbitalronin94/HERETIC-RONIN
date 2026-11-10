import json
import tempfile
import unittest
from pathlib import Path

import torch

from heretic_ronin import HereticConfig, HereticRoninLM
from scripts.build_heretic_tokenizer import build_tokenizer


class HereticModelTests(unittest.TestCase):
    def test_all_parameters_trainable_and_embeddings_tied(self):
        config = HereticConfig(
            vocab_size=350, context_length=32, n_layers=2,
            d_model=32, n_heads=4, d_ff=64,
            gradient_checkpointing=False,
        )
        model = HereticRoninLM(config)
        model.assert_fully_trainable()
        self.assertEqual(
            model.token_embedding.weight.data_ptr(),
            model.lm_head.weight.data_ptr(),
        )
        self.assertTrue(all(p.requires_grad for p in model.parameters()))

    def test_causal_lm_loss_is_finite(self):
        config = HereticConfig(
            vocab_size=512, context_length=16, n_layers=1,
            d_model=16, n_heads=4, d_ff=32,
            gradient_checkpointing=False,
        )
        model = HereticRoninLM(config)
        ids = torch.randint(0, config.vocab_size, (2, 8))
        _, loss = model(ids, labels=ids)
        self.assertIsNotNone(loss)
        self.assertTrue(torch.isfinite(loss).item())


class HereticTokenizerTests(unittest.TestCase):
    def test_byte_level_bpe_round_trip_multilingual(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "train.jsonl"
            samples = [
                "Español: áéíóú, ñ, ¿qué tal?",
                "Català: llengua, ciència i programació.",
                "English: transformer attention and tokenization.",
                "Matemáticas: ∑ ∫ π → lógica.",
            ] * 20
            corpus.write_text(
                "".join(json.dumps({"text": value}, ensure_ascii=False) + "\n"
                        for value in samples),
                encoding="utf-8",
            )
            tokenizer = build_tokenizer([corpus], vocab_size=512)
            for sample in samples:
                encoded = tokenizer.encode(sample)
                decoded = tokenizer.decode(encoded.ids, skip_special_tokens=True)
                self.assertEqual(decoded, sample)


if __name__ == "__main__":
    unittest.main()
