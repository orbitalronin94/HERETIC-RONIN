import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import review_candidate_samples


class CandidateSamplePrivacyTests(unittest.TestCase):
    def test_stdout_contains_summary_not_sample_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.jsonl"
            source.write_text(json.dumps({
                "source": "example/source",
                "revision": "abc123",
                "config": "default",
                "license": "CC0-1.0",
                "source_metadata": {"language": "es", "domain": "science"},
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
            self.assertNotIn('"text"', logged)
            summary = json.loads(logged)
            self.assertEqual(summary["sources"][0]["sample_count"], 1)
            self.assertEqual(summary["sources"][0]["rows"], 1)
            private_review = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(private_review["sources"][0]["samples"][0]["text"],
                             "PRIVATE_SAMPLE_TEXT_MUST_NOT_REACH_PUBLIC_LOGS")

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

if __name__ == "__main__":
    unittest.main()
