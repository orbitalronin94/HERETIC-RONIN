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

    def test_eprs_publications_require_item_level_cc_by_and_remain_discovery_only(self):
        source = self.source("European Parliament:Think Tank-EPRS-CC-BY-4.0-item-level")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertIn("own item page", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("individual publication page", " ".join(source["required_checks"]))
        self.assertGreaterEqual(len(source["evidence_urls"]), 4)
        self.assertGreaterEqual(len(source["required_checks"]), 10)

    def test_cordis_scope_is_limited_to_eu_owned_editorial_content_and_excludes_beneficiary_material(self):
        source = self.source("CORDIS:EU-owned-editorial-news-and-thematic-packs-CC-BY-4.0")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertIn("EU-owned editorial content", source["reported_license"])
        self.assertIn("beneficiary", source["rights_caveat"])
        self.assertIn("personal data", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("grant", checks)
        self.assertIn("global g-0", checks)
        self.assertIn("machine-translated", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 3)
        self.assertGreaterEqual(len(source["required_checks"]), 12)

    def test_open_research_europe_requires_item_level_cc_by_approved_peer_review_and_global_g0(self):
        source = self.source("Open Research Europe:CC-BY-4.0-item-level-research-articles")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertIn("individual articles", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("peer-review", checks)
        self.assertIn("global g-0", checks)
        self.assertIn("version doi", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)
        self.assertGreaterEqual(len(source["required_checks"]), 12)

    def test_council_register_remains_unlicensed_for_automatic_training_pending_item_checks(self):
        source = self.source("Council of the European Union:public-register-of-council-documents")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIn("LicenseRef-Council-Decision-2017-1842", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("adaptation", source["reported_license"])
        self.assertGreaterEqual(len(source["evidence_urls"]), 3)
        self.assertGreaterEqual(len(source["required_checks"]), 9)


    def test_plos_articles_require_exact_item_level_cc_by_and_global_g0(self):
        source = self.source("PLOS:research-articles-item-level-CC-BY-4.0")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0"])
        self.assertIn("exact item-level", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("10 requests/minute", checks)
        self.assertIn("jats xml", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 4)
        self.assertGreaterEqual(len(source["required_checks"]), 12)

    def test_wipo_publications_are_limited_to_item_level_cc_by_4_and_third_party_clearance(self):
        source = self.source("WIPO:online-publications-item-level-CC-BY-4.0")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0"])
        self.assertIn("individual", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("copyright-notice", checks)
        self.assertIn("doi/isbn", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)
        self.assertGreaterEqual(len(source["required_checks"]), 12)

    def test_wipo_lex_is_blocked_for_noncommercial_and_bulk_automation_terms(self):
        source = self.source("WIPO Lex:IP-legal-texts-translations-and-judgments")
        self.assertTrue(source["status"].startswith("blocked_"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("Not measured", source["reported_size"])
        self.assertIsNone(source.get("spdx_license_identifier"))
        terms = " ".join([source["reported_license"], source["rights_caveat"], *source["required_checks"]]).casefold()
        self.assertIn("non-commercial", terms)
        self.assertIn("automated queries", terms)
        self.assertIn("bulk", terms)
        self.assertGreaterEqual(len(source["evidence_urls"]), 2)
    def test_latest_scheduled_acquisitions_are_verified_zero_byte_storage_blocks(self):
        last = self.registry["last_candidate_batch_details"]
        previous = self.registry["previous_candidate_batch_details"]
        self.assertEqual(last["run_id"], 44262175192)
        self.assertEqual(previous["run_id"], 44177892230)
        self.assertEqual(last["source_group"], 5)
        self.assertEqual(previous["source_group"], 3)
        self.assertEqual(last["artifact_sha256"], "0f4c06392971fb32a751e5878d6737deed43aa98196b002ff637ccf58ae7a650")
        self.assertEqual(last["manifest_sha256"], "0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7")
        self.assertEqual(previous["artifact_sha256"], "f6099c982aa2fe7a1ab0500f6fac06279223a46b59757849a8fdc7aed01cc4a8")
        self.assertEqual(previous["manifest_sha256"], "2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26")
        for batch in (last, previous):
            self.assertEqual(batch["candidate_rows"], 0)
            self.assertEqual(batch["downloaded_jsonl_bytes_in_runner"], 0)
            self.assertEqual(batch["retained_payload_bytes"], 0)
            self.assertEqual(batch["admitted_bytes_added"], 0)
            self.assertIs(batch["training_authorized"], False)
            self.assertIs(batch["checks"]["payload_downloaded"], False)
            self.assertEqual(batch["storage_gate"]["status"], "blocked")
            self.assertEqual(batch["manifest_bytes"], 871)
            self.assertEqual(batch["artifact_zip_bytes"], 653)


if __name__ == "__main__":
    unittest.main()
