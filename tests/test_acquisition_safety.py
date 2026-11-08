import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from scripts.acquisition_safety import (
    AtomicCandidateWriter,
    finalize_candidate_file,
    json_default,
)


class AcquisitionSafetyTests(unittest.TestCase):
    def test_datetime_uses_iso8601(self):
        value = datetime(2026, 11, 8, 12, 30, tzinfo=timezone.utc)
        self.assertEqual(json.dumps({"date": value}, default=json_default),
                         '{"date": "2026-11-08T12:30:00+00:00"}')

    def test_date_uses_iso8601(self):
        self.assertEqual(json_default(date(2026, 11, 8)), "2026-11-08")

    def test_unknown_object_fails_closed(self):
        with self.assertRaises(TypeError):
            json_default(object())

    def test_writer_removes_partial_file_when_producer_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            partial = Path(directory) / "shard.jsonl.partial"
            with self.assertRaises(RuntimeError):
                with AtomicCandidateWriter(partial) as handle:
                    handle.write('{"text":"partial"}\\n')
                    raise RuntimeError("simulated stream failure")
            self.assertFalse(partial.exists())

    def test_below_minimum_discards_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            partial = Path(directory) / "shard.jsonl.partial"
            target = Path(directory) / "shard.jsonl"
            partial.write_text('{"text":"not enough"}\\n', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "partial shard discarded"):
                finalize_candidate_file(partial, target, 1, 2, "fixture/source")
            self.assertFalse(partial.exists())
            self.assertFalse(target.exists())

    def test_complete_shard_is_atomically_published(self):
        with tempfile.TemporaryDirectory() as directory:
            partial = Path(directory) / "shard.jsonl.partial"
            target = Path(directory) / "shard.jsonl"
            partial.write_text('{"text":"ok"}\\n', encoding="utf-8")
            finalize_candidate_file(partial, target, 2, 2, "fixture/source")
            self.assertFalse(partial.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), '{"text":"ok"}\\n')


if __name__ == "__main__":
    unittest.main()
