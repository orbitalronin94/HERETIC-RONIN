import json
import unittest
from pathlib import Path

from scripts.license_gates import license_values_allowed


class LicenseGateTests(unittest.TestCase):
    def test_cc_by_sa_does_not_match_cc_by_prefix(self):
        self.assertFalse(license_values_allowed(
            "https://creativecommons.org/licenses/by-sa/4.0/",
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]},
        ))

    def test_exact_uri_matches_case_and_trailing_slash(self):
        self.assertTrue(license_values_allowed(
            "HTTPS://CREATIVECOMMONS.ORG/LICENSES/BY/4.0/",
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0"]},
        ))

    def test_common_pile_cc_by_descriptor_matches_exact_uri(self):
        self.assertTrue(license_values_allowed(
            "Creative Commons - Attribution - https://creativecommons.org/licenses/by/4.0/",
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0/", "http://creativecommons.org/licenses/by/4.0/"]},
        ))

    def test_common_pile_cc0_descriptor_matches_exact_uri(self):
        self.assertTrue(license_values_allowed(
            "Creative Commons Zero - Public Domain - https://creativecommons.org/publicdomain/zero/1.0/",
            {"license_filter": ["https://creativecommons.org/publicdomain/zero/1.0/", "http://creativecommons.org/publicdomain/zero/1.0/"]},
        ))

    def test_common_pile_sharealike_descriptor_does_not_match_cc_by(self):
        self.assertFalse(license_values_allowed(
            "Creative Commons - Attribution Share-Alike - https://creativecommons.org/licenses/by-sa/4.0/",
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]},
        ))

    def test_descriptor_label_must_match_uri(self):
        self.assertFalse(license_values_allowed(
            "Creative Commons - Attribution Share-Alike - https://creativecommons.org/licenses/by/4.0/",
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]},
        ))

    def test_unrecognised_or_embellished_descriptor_fails_closed(self):
        self.assertFalse(license_values_allowed(
            "Creative Commons - Attribution - https://creativecommons.org/licenses/by/4.0/ with extra terms",
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]},
        ))

    def test_unknown_and_missing_license_fail_closed(self):
        allowed = {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]}
        self.assertFalse(license_values_allowed(None, allowed))
        self.assertFalse(license_values_allowed("", allowed))
        self.assertFalse(license_values_allowed("unknown", allowed))

    def test_license_array_with_missing_entry_fails_closed(self):
        self.assertFalse(license_values_allowed(
            ["https://creativecommons.org/licenses/by/4.0/", None],
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]},
        ))
        self.assertFalse(license_values_allowed(
            ["https://creativecommons.org/licenses/by/4.0/", ""],
            {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]},
        ))

    def test_combined_license_string_is_not_split_or_accepted(self):
        self.assertFalse(license_values_allowed(
            "CC-BY-4.0; CC0-1.0",
            {"license_exact_allowlist": ["CC-BY-4.0", "CC0-1.0"]},
        ))

    def test_mixed_license_array_requires_every_value_to_be_allowed(self):
        self.assertFalse(license_values_allowed(
            ["CC-BY-4.0", "CC-BY-NC-4.0"],
            {"license_all_exact_allowlist": ["CC-BY-4.0", "CC0-1.0"]},
        ))
        self.assertTrue(license_values_allowed(
            ["CC-BY-4.0", "CC0-1.0"],
            {"license_all_exact_allowlist": ["CC-BY-4.0", "CC0-1.0"]},
        ))

    def test_license_name_is_exact_not_substring(self):
        self.assertFalse(license_values_allowed(
            "Apache License 2.0 with additional restrictions",
            {"license_name_filter": ["Apache License 2.0"]},
        ))
        self.assertTrue(license_values_allowed(
            "Apache License 2.0",
            {"license_name_filter": ["Apache License 2.0"]},
        ))

    def test_multiple_constraints_must_all_pass(self):
        self.assertFalse(license_values_allowed(
            "CC-BY-4.0",
            {
                "license_exact_allowlist": ["CC-BY-4.0"],
                "license_name_filter": ["MIT License"],
            },
        ))

    def test_sources_without_record_level_allowlist_are_unchanged(self):
        self.assertTrue(license_values_allowed(None, {}))

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

    def test_french_assembly_debates_remain_discovery_only(self):
        from pathlib import Path
        import json

        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        matches = [
            source for source in registry["sources"]
            if source.get("id") == "Assemblée nationale:an-comptes-rendus-17e"
        ]
        self.assertEqual(len(matches), 1)
        source = matches[0]
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("Not measured", source["reported_size"])
        self.assertIn("LicenseRef-Etalab-Open-License-v1.0", source["reported_license"])
        self.assertIn("personal data", source["rights_caveat"])
        self.assertEqual(source["publisher_checksums"]["md5"], "a91c9d51574a8e89eb183a7bef74bf57")
        self.assertIn("SHA-256", source["revision"])


    def test_boe_consolidated_legislation_remains_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Agencia Estatal BOE:legislacion-consolidada")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("LicenseRef-BOE-Reuse-2024", source["reported_license"])
        self.assertIn("Biblioteca Jurídica Digital", source["rights_caveat"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_legifrance_api_remains_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "DILA/Légifrance:legal-texts-api-open-2.0")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("LicenseRef-Etalab-Open-License-2.0", source["reported_license"])
        self.assertIn("PISTE", source["reported_size"])
        self.assertIn("personal-data", source["rights_caveat"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_bundestag_payload_is_blocked_without_explicit_license(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Deutscher Bundestag:plenarprotokolle-und-drucksachen")
        self.assertTrue(source["status"].startswith("blocked_discovery"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("No explicit licence", source["reported_license"])

    def test_govinfo_is_blocked_pending_territorial_and_third_party_review(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "US GovInfo:USCODE-CFR-STATUTE")
        self.assertTrue(source["status"].startswith("blocked_discovery"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("17 U.S.C. §105", source["reported_license"])
        self.assertIn("Spain", source["rights_caveat"])

    def test_stortinget_nlod_candidate_remains_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Stortinget:open-data-api")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("LicenseRef-NLOD-2.0", source["reported_license"])
        self.assertIn("100 requests per minute", source["reported_license"])
        self.assertIn("personal data", source["rights_caveat"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_folketinget_transcripts_are_blocked_pending_special_rights_review(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Folketinget:open-data-proceedings")
        self.assertTrue(source["status"].startswith("blocked_discovery"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("exclusive right", source["reported_license"])
        self.assertIn("collections of their own contributions", source["rights_caveat"])


    def test_ilo_research_repository_remains_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "International Labour Organization:research-repository-cc-by-2023-05-03+")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("2023-05-03", source["reported_license"])
        self.assertIn("copyright page", " ".join(source["required_checks"]))
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("microdata", source["rights_caveat"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_australian_federal_register_remains_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Australia Federal Register of Legislation:commonwealth-laws-cc-by-4.0-default")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("CC BY 4.0", source["reported_license"])
        self.assertIn("Third-party", source["reported_license"])
        self.assertIn("F2014L01500", source["reported_license"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_canadian_justice_laws_remains_blocked_on_adaptation_scope(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Canada Justice Laws:consolidated-federal-laws-bulk-xml")
        self.assertTrue(source["status"].startswith("blocked_discovery"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("OGL Canada 2.0", source["reported_license"])
        self.assertIn("Reproduction of Federal Law Order", source["reported_license"])
        self.assertIn("adaptation", source["rights_caveat"])

    def test_run_88_candidate_batch_is_not_counted_as_admitted_or_staged(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        batch = next(x for x in registry["historical_candidate_batches"] if x["run_id"] == 43176267906)
        self.assertEqual(batch["run_id"], 43176267906)
        self.assertEqual(batch["candidate_rows"], 170000)
        self.assertEqual(batch["candidate_jsonl_bytes"], 462861425)
        self.assertEqual(batch["staged_rows"], 0)
        self.assertEqual(batch["retained_payload_bytes"], 0)
        self.assertEqual(batch["admitted_rows_added"], 0)
        self.assertEqual(batch["admitted_bytes_added"], 0)
        self.assertIs(batch["training_authorized"], False)
        self.assertEqual(batch["artifact_sha256"], "87b93844e6b74ee1eb23468d86055e588e0c142510cf26ee905d3342fccf3626")
        self.assertEqual(batch["manifest_sha256"], "3f1fa4f320b866dcb85ef7910b7d78646f7bcf97ae36daf4108836c479ea1a83")


    def test_run_87_artifact_publication_failure_is_not_staged_or_admitted(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        batch = next(x for x in registry["historical_candidate_batches"] if x["run_id"] == 43090663647)
        self.assertEqual(batch["run_id"], 43090663647)
        self.assertEqual(batch["conclusion"], "failure")
        self.assertEqual(batch["candidate_rows"], 73736)
        self.assertEqual(batch["candidate_jsonl_bytes"], 807461935)
        self.assertIs(batch["manifest_available"], False)
        self.assertIsNone(batch["artifact_id"])
        self.assertEqual(batch["staged_rows"], 0)
        self.assertEqual(batch["retained_payload_bytes"], 0)
        self.assertEqual(batch["admitted_rows_added"], 0)
        self.assertEqual(batch["admitted_bytes_added"], 0)
        self.assertIs(batch["training_authorized"], False)
        self.assertIn("failed to create", batch["artifact_failure"])

    def test_run_92_candidate_batch_is_not_staged_or_admitted(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        batch = next(x for x in registry["historical_candidate_batches"] if x["run_id"] == 43298985874)
        self.assertEqual(batch["run_id"], 43298985874)
        self.assertEqual(batch["candidate_rows"], 35000)
        self.assertEqual(batch["candidate_jsonl_bytes"], 945924928)
        self.assertEqual(batch["staged_rows"], 0)
        self.assertEqual(batch["retained_payload_bytes"], 0)
        self.assertEqual(batch["admitted_bytes_added"], 0)
        self.assertEqual(batch["manifest_sha256"], "c4d9055db2c098b1f05c6333c60df18636f74e125d65e7ea7ba57881c6296645")

    def test_run_93_is_an_exact_duplicate_of_run_87_and_not_admitted(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        batch = next(x for x in registry["historical_candidate_batches"] if x["run_id"] == 43383222519)
        self.assertEqual(batch["run_id"], 43383222519)
        self.assertEqual(batch["duplicate_of_run_id"], 43090663647)
        self.assertEqual(batch["unique_candidate_rows_added"], 0)
        self.assertEqual(batch["unique_candidate_bytes_added"], 0)
        self.assertEqual(batch["candidate_rows"], 73736)
        self.assertEqual(batch["candidate_jsonl_bytes"], 807461935)
        self.assertEqual(batch["staged_rows"], 0)
        self.assertEqual(batch["admitted_bytes_added"], 0)
        self.assertEqual(batch["artifact_sha256"], "79b3e47ad7467370f611b979bd7294a1022f6f114eca6ce4b59d075218965129")
        historical = next(x for x in registry["historical_candidate_batches"] if x["run_id"] == 43090663647)
        self.assertEqual(historical["candidate_sources"][0]["sha256"], batch["candidate_sources"][0]["sha256"])

    def test_eurostat_candidate_is_scoped_and_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Eurostat:statistics-data-metadata-publications")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("2011/833/EU", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("historical versions are not retained", source["revision"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_oecd_candidate_is_post_2024_cc_by_only_and_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "OECD:written-content-cc-by-4.0-from-2024-07-01")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertIn("2024-07-01", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_openthoughts3_is_held_and_not_reacquired_until_source_lineage_is_cleared(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "open-thoughts/OpenThoughts3-1.2M")
        self.assertTrue(source["status"].startswith("held_downloaded_ephemeral"))
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIs(source["training_authorized"], False)
        self.assertEqual(source["last_acquisition"]["run_id"], 43298985874)
        self.assertEqual(source["last_acquisition"]["durable_staged_rows"], 0)
        self.assertEqual(source["last_acquisition"]["admitted_rows"], 0)
        script = (root / "scripts/acquire_open_source_candidates.py").read_text(encoding="utf-8")
        self.assertIn('"enabled":False', script)
        self.assertIn("held_source_disabled", script)

    def test_run_102_storage_gate_blocked_before_download_and_not_admitted(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        batch = next(x for x in registry["historical_candidate_batches"] if x["run_id"] == 43568604566)
        self.assertEqual(batch["conclusion"], "success")
        self.assertEqual(batch["candidate_rows"], 0)
        self.assertEqual(batch["candidate_jsonl_bytes"], 0)
        self.assertEqual(batch["staged_rows"], 0)
        self.assertEqual(batch["retained_payload_bytes"], 0)
        self.assertEqual(batch["admitted_rows_added"], 0)
        self.assertEqual(batch["admitted_bytes_added"], 0)
        self.assertIs(batch["training_authorized"], False)
        self.assertIs(batch["storage_gate"]["payload_downloaded"], False)
        self.assertEqual(batch["storage_gate"]["status"], "blocked")
        self.assertEqual(batch["artifact_sha256"], "88c9315417f8f9cb6531c0ed8df6b7b9bb79d240bae86163c94bef75753fb5da")
        self.assertEqual(batch["manifest_sha256"], "0a917a1e504cddc4373d3f5d0be3d3b74f24e47d71bc765236bbfcdfa9b658c7")

    def test_eurovoc_424_remains_discovery_only_until_current_distribution_license_is_verified(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "Publications Office EU:EuroVoc-4.24-multilingual-thesaurus")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["reported_rows"])
        self.assertIn("4.24", source["revision"])
        self.assertIn("2020", source["reported_license"])
        self.assertIn("current 4.24 release's own distribution licence has not yet been confirmed", source["reported_license"])
        self.assertEqual(len(source["language"]), 27)
        self.assertGreaterEqual(len(source["required_checks"]), 8)

    def test_hudoc_is_blocked_under_noncommercial_reuse_terms(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "European Court of Human Rights:HUDOC-case-law")
        self.assertTrue(source["status"].startswith("blocked_noncommercial"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("prior written permission", source["reported_license"])
        self.assertIn("commercial", source["reported_license"])

    def test_public_encryption_uses_explicit_high_work_factor(self):
        root = Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/acquire-open-source-candidates.yml").read_text(encoding="utf-8")
        command = next(line.strip() for line in workflow.splitlines() if "gpg --batch --yes --pinentry-mode loopback --symmetric" in line and '--output "$encrypted"' in line)
        self.assertIn("--cipher-algo AES256", command)
        self.assertIn("--s2k-digest-algo SHA512", command)
        self.assertIn("--s2k-mode 3", command)
        self.assertIn("--s2k-count 65011712", command)

    def test_eea_wise_records_are_item_scoped_discovery_only(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "European Environment Agency:EEA-Datahub-WISE-CC-BY-4.0-records")
        self.assertTrue(source["status"].startswith("candidate_discovery_only"))
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIn("c6e353a2-c004-41eb-b0c1-5a2a1da5ef3b", source["revision"])
        self.assertIn("3c13b52b-36e5-44bc-a07f-8389d43dfd3b", source["revision"])
        self.assertIn("third parties", source["reported_license"])
        self.assertGreaterEqual(len(source["required_checks"]), 9)

    def test_fao_default_noncommercial_terms_are_blocked(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        source = next(s for s in registry["sources"] if s.get("id") == "FAO:publications-document-repository-default-terms")
        self.assertTrue(source["status"].startswith("blocked_noncommercial"))
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIn("non-commercial", source["reported_license"])
        self.assertIn("permission request", source["reported_license"])


    def test_run_101_storage_gate_manifest_is_verified_and_not_admitted(self):
        root = Path(__file__).resolve().parents[1]
        registry = json.loads((root / "data/sources/registry.json").read_text(encoding="utf-8"))
        batch = next(x for x in registry["historical_candidate_batches"] if x["run_id"] == 43496984977)
        self.assertEqual(batch["conclusion"], "success")
        self.assertEqual(batch["source_group"], 3)
        self.assertEqual(batch["candidate_rows"], 0)
        self.assertEqual(batch["candidate_jsonl_bytes"], 0)
        self.assertEqual(batch["artifact_sha256"], "cddd161c01910852db6083f15ed157b2b4c6e2ad38308fa5ddc070b9767205b6")
        self.assertEqual(batch["manifest_sha256"], "2829acd2e3d3d88cd5d58aa573fff9cfc9c9067d45dc1035e09e1c190c488b26")
        self.assertEqual(batch["retained_payload_bytes"], 0)
        self.assertEqual(batch["admitted_bytes_added"], 0)
        self.assertIs(batch["training_authorized"], False)
        self.assertIs(batch["storage_gate"]["payload_downloaded"], False)


if __name__ == "__main__":
    unittest.main()
