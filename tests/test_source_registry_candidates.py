import json
import unittest
from pathlib import Path


class SourceRegistryCandidateTests(unittest.TestCase):
    def test_austrian_parliament_transcripts_remain_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        matches = [
            source for source in registry["sources"]
            if source.get("id") == "Austrian Parliament:stenographic-protocols-nationalrat-bundesrat"
        ]
        self.assertEqual(len(matches), 1)
        source = matches[0]
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("Not measured", source["reported_size"])
        self.assertIn("freie Werke", source["reported_license"])
        self.assertIn("CC-BY-4.0", source["reported_license"])
        self.assertIn("SHA-256", source["revision"])
        self.assertIn("exact POST body", source["revision"])
        self.assertTrue(source["evidence_urls"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)


if __name__ == "__main__":
    unittest.main()
