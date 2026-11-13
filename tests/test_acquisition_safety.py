import json
import tempfile
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from scripts.acquisition_safety import (
    AtomicCandidateWriter,
    finalize_candidate_file,
    json_default,
    select_source_group,
    scheduled_source_group,
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
                    handle.write('{"text":"partial"}\n')
                    raise RuntimeError("simulated stream failure")
            self.assertFalse(partial.exists())

    def test_below_minimum_discards_partial_file(self):
        with tempfile.TemporaryDirectory() as directory:
            partial = Path(directory) / "shard.jsonl.partial"
            target = Path(directory) / "shard.jsonl"
            partial.write_text('{"text":"not enough"}\n', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "partial shard discarded"):
                finalize_candidate_file(partial, target, 1, 2, "fixture/source")
            self.assertFalse(partial.exists())
            self.assertFalse(target.exists())

    def test_complete_shard_is_atomically_published(self):
        with tempfile.TemporaryDirectory() as directory:
            partial = Path(directory) / "shard.jsonl.partial"
            target = Path(directory) / "shard.jsonl"
            partial.write_text('{"text":"ok"}\n', encoding="utf-8")
            finalize_candidate_file(partial, target, 2, 2, "fixture/source")
            self.assertFalse(partial.exists())
            self.assertEqual(target.read_text(encoding="utf-8"), '{"text":"ok"}\n')


    def test_source_groups_are_disjoint_and_cover_every_source_for_four_and_eight_groups(self):
        sources = [{"id": f"source-{i}"} for i in range(41)]
        for group_count in (4, 8):
            with self.subTest(group_count=group_count):
                groups = [
                    select_source_group(sources, group_index, group_count)
                    for group_index in range(group_count)
                ]
                flattened = [index for group in groups for index, _ in group]
                self.assertEqual(sorted(flattened), list(range(len(sources))))
                self.assertEqual(len(flattened), len(set(flattened)))

    def test_scheduled_groups_cover_all_eight_groups_once_every_48_hours(self):
        first_cycle = [
            scheduled_source_group(day, slot, 8, 4)
            for day in (1, 2)
            for slot in range(4)
        ]
        second_cycle = [
            scheduled_source_group(day, slot, 8, 4)
            for day in (3, 4)
            for slot in range(4)
        ]
        self.assertEqual(first_cycle, list(range(8)))
        self.assertEqual(second_cycle, list(range(8)))

    def test_scheduled_group_rejects_invalid_day_slot_and_counts(self):
        with self.assertRaises(ValueError):
            scheduled_source_group(0, 0, 8, 4)
        with self.assertRaises(ValueError):
            scheduled_source_group(367, 0, 8, 4)
        with self.assertRaises(ValueError):
            scheduled_source_group(1, 4, 8, 4)
        with self.assertRaises(ValueError):
            scheduled_source_group(1, 0, 0, 4)

    def test_source_group_rejects_invalid_bounds(self):
        sources = [{"id": "one"}]
        with self.assertRaises(ValueError):
            select_source_group(sources, 0, 0)
        with self.assertRaises(ValueError):
            select_source_group(sources, -1, 4)
        with self.assertRaises(ValueError):
            select_source_group(sources, 4, 4)


    def test_workflow_schedule_uses_configured_group_count(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/acquire-open-source-candidates.yml").read_text(encoding="utf-8")
        self.assertIn('HERETIC_SOURCE_GROUP_COUNT: "8"', workflow)
        self.assertIn('HERETIC_SOURCE_GROUP_SLOTS_PER_DAY: "4"', workflow)
        self.assertIn('scheduled_source_group', workflow)
        self.assertNotIn('  push:\n    branches: [main]', workflow)
        self.assertIn('Check durable candidate storage before downloading', workflow)
        self.assertIn('HERETIC_STAGING_PASSPHRASE', workflow)
        self.assertIn('gpg --batch', workflow)
        self.assertIn('blocked_storage_gate', workflow)

if __name__ == "__main__":
    unittest.main()
