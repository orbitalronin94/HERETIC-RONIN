import json
import unittest
from pathlib import Path


class RegistryCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[1]
        cls.registry = json.loads(
            (root / "data/sources/registry.json").read_text(encoding="utf-8")
        )

    def source(self, source_id):
        matches = [s for s in self.registry["sources"] if s.get("id") == source_id]
        self.assertEqual(len(matches), 1)
        return matches[0]

    def assert_discovery_only(self, source):
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("Not measured", source["reported_size"])

    def test_uk_legislation_is_scoped_to_ogl_and_excludes_eurlex_derived_material(self):
        source = self.source("UK legislation:legislation.gov.uk-core-text-OGL-UK-3.0")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "OGL-UK-3.0")
        self.assertIn("derived from EUR-Lex", source["reported_license"])
        self.assertIn("Westlaw", source["rights_caveat"])
        self.assertIn("personal data", source["rights_caveat"])
        self.assertIn("versioned URI", " ".join(source["required_checks"]))
        self.assertGreaterEqual(len(source["evidence_urls"]), 6)
        self.assertGreaterEqual(len(source["required_checks"]), 10)

    def test_council_register_remains_unlicensed_for_automatic_training_pending_item_checks(self):
        source = self.source("Council of the European Union:public-register-of-council-documents")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIn("LicenseRef-Council-Decision-2017-1842", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("adaptation", source["reported_license"])
        self.assertGreaterEqual(len(source["evidence_urls"]), 3)
        self.assertGreaterEqual(len(source["required_checks"]), 9)


if __name__ == "__main__":
    unittest.main()
