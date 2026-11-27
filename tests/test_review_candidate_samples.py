import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import review_candidate_samples


class CandidateSamplePrivacyTests(unittest.TestCase):
    def test_stdout_contains_summary_not_sample_text_and_private_output_is_stratified(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.jsonl"
            source.write_text(json.dumps({
                "source": "example/source",
                "revision": "abc123",
                "config": "default",
                "license": "CC0-1.0",
                "source_metadata": {
                    "language": "es",
                    "domain": "science",
                    "worker_id": "MUST_NOT_BE_RETAINED",
                    "speaker_id": "MUST_NOT_BE_RETAINED",
                    "gender": "MUST_NOT_BE_RETAINED",
                },
                "text": "PRIVATE_SAMPLE_TEXT_MUST_NOT_REACH_PUBLIC_LOGS"
            }) + chr(10), encoding="utf-8")
            output = root / "MANUAL-SAMPLE-REVIEW.json"
            stdout = io.StringIO()
            with patch.object(review_candidate_samples, "ROOT", root), \
                 patch.object(review_candidate_samples, "OUT", output), \
                 contextlib.redirect_stdout(stdout):
                review_candidate_samples.main()
            logged = stdout.getvalue()
            self.assertNotIn("PRIVATE_SAMPLE_TEXT_MUST_NOT_REACH_PUBLIC_LOGS", logged)
            self.assertNotIn("MUST_NOT_BE_RETAINED", logged)
            self.assertNotIn('"text"', logged)
            summary = json.loads(logged)
            self.assertEqual(summary["sources"][0]["sample_count"], 1)
            self.assertEqual(summary["sources"][0]["rows"], 1)
            self.assertEqual(summary["stratification"], ["source", "domain", "language", "format"])
            private_review = json.loads(output.read_text(encoding="utf-8"))
            sample = private_review["sources"][0]["samples"][0]
            self.assertEqual(sample["text"], "PRIVATE_SAMPLE_TEXT_MUST_NOT_REACH_PUBLIC_LOGS")
            self.assertEqual(sample["stratum"], {
                "domain": "science",
                "language": "es",
                "format": "unknown",
            })
            self.assertNotIn("worker_id", sample["source_metadata"])
            self.assertNotIn("speaker_id", sample["source_metadata"])
            self.assertNotIn("gender", sample["source_metadata"])

    def test_samples_cover_observed_domain_language_and_format_strata(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "multi.jsonl"
            rows = [
                {"source": "multi", "revision": "r1", "license": "CC0-1.0",
                 "source_metadata": {"domain": "math", "language": "es", "format": "text/plain"},
                 "text": "Mathematics in Spanish with plain text format."},
                {"source": "multi", "revision": "r1", "license": "CC0-1.0",
                 "source_metadata": {"domain": "science", "language": "en", "format": "application/xml"},
                 "text": "Science in English with XML format."},
                {"source": "multi", "revision": "r1", "license": "CC0-1.0",
                 "source_metadata": {"domain": "science", "language": "fr", "format": "application/pdf"},
                 "text": "Science in French with PDF source format."},
                {"source": "multi", "revision": "r1", "license": "CC0-1.0",
                 "source_metadata": {"domain": "law", "language": "de", "format": "application/xml"},
                 "text": "Law in German with XML source format."},
            ]
            source.write_text(
                "".join(json.dumps(row) + "\n" for row in rows),
                encoding="utf-8",
            )
            output = root / "MANUAL-SAMPLE-REVIEW.json"
            stdout = io.StringIO()
            with patch.object(review_candidate_samples, "ROOT", root), \
                 patch.object(review_candidate_samples, "OUT", output), \
                 contextlib.redirect_stdout(stdout):
                review_candidate_samples.main()
            report = json.loads(output.read_text(encoding="utf-8"))
            samples = report["sources"][0]["samples"]
            self.assertEqual(report["stratification"], ["source", "domain", "language", "format"])
            self.assertEqual({item["stratum"]["domain"] for item in samples}, {"math", "science", "law"})
            self.assertEqual({item["stratum"]["language"] for item in samples}, {"es", "en", "fr", "de"})
            self.assertEqual(
                {item["stratum"]["format"] for item in samples},
                {"text/plain", "application/xml", "application/pdf"},
            )
            summary = json.loads(stdout.getvalue())
            self.assertEqual(summary["sources"][0]["coverage"]["domain"]["observed_values"], 3)
            self.assertEqual(summary["sources"][0]["coverage"]["language"]["sampled_values"], 4)
            self.assertEqual(summary["sources"][0]["coverage"]["format"]["sampled_values"], 3)

    def test_workflow_gates_raw_artifact_on_private_repository(self):
        workflow = Path(".github/workflows/acquire-open-source-candidates.yml").read_text(encoding="utf-8")
        private_step = workflow.split("name: Upload private candidate tranche and sample report", 1)[1].split("      - name:", 1)[0]
        public_step = workflow.split("name: Upload public manifest only (no payloads or sample text)", 1)[1].split("      - name:", 1)[0]
        self.assertIn("github.event.repository.private == true", private_step)
        self.assertIn("github.event.repository.private != true", public_step)
        self.assertEqual(public_step.count("staging/open-source-candidates/OPEN-SOURCE-MANIFEST.json"), 1)
        self.assertNotIn("staging/open-source-candidates/**/*.jsonl", public_step)
        self.assertNotIn("!staging/open-source-candidates", public_step)

    def test_public_candidate_artifact_requires_encryption_or_skips_download(self):
        workflow = Path(".github/workflows/acquire-open-source-candidates.yml").read_text(encoding="utf-8")
        self.assertIn("Check durable candidate storage before downloading", workflow)
        self.assertIn("steps.storage.outputs.ready == 'true'", workflow)
        self.assertIn("steps.storage.outputs.ready != 'true'", workflow)
        self.assertIn("Encrypt candidate tranche before public artifact upload", workflow)
        self.assertIn("Upload encrypted candidate tranche (public repository)", workflow)
        self.assertIn("Remove any plaintext candidate payload after public packaging", workflow)
        self.assertIn("retention-days: 90", workflow)
        self.assertIn("blocked_storage_gate", workflow)
        self.assertIn("HERETIC_STAGING_PASSPHRASE", workflow)
        self.assertIn("32", workflow)
        self.assertIn("65011712", workflow)
        self.assertIn("Smoke-test GPG AES-256 candidate packaging with a disposable fixture", workflow)
        self.assertIn('cmp "$tmp/plain.txt" "$tmp/roundtrip.txt"', workflow)

    def test_workflow_runs_the_stratified_review_step_without_logging_excerpts(self):
        workflow = Path(".github/workflows/acquire-open-source-candidates.yml").read_text(encoding="utf-8")
        self.assertIn("stratified by source/domain/language/format", workflow)
        self.assertIn("python scripts/review_candidate_samples.py", workflow)
        self.assertIn("without logging excerpts", workflow)


if __name__ == "__main__":
    unittest.main()
