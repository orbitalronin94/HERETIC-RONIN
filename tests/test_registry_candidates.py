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
        self.assertIn("item-level", source["reported_license"])
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

    def test_open_book_publishers_requires_per_title_cc_by_4_and_component_clearance(self):
        source = self.source("Open Book Publishers:peer-reviewed-books-item-level-CC-BY-4.0")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0"])
        self.assertIn("authors retain copyright", source["reported_license"])
        self.assertIn("CC BY-SA 4.0", source["reported_license"])
        self.assertIn("chapter-level", source["rights_caveat"])
        self.assertIn("fair-use", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("exact cc by 4.0", checks)
        self.assertIn("global g-0", checks)
        self.assertIn("sha-256", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 7)
        self.assertGreaterEqual(len(source["required_checks"]), 14)

    def test_canada_justice_laws_bulk_xml_is_item_level_ogl_candidate_only(self):
        source = self.source("Canada Justice Laws:consolidated-federal-laws-bulk-xml")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "LicenseRef-OGL-Canada-2.0")
        self.assertIn("Open Government Portal", source["reported_license"])
        self.assertIn("LICENSE.md", source["reported_license"])
        self.assertIn("855cdfc65207a6906c414e09a77d7f93267c5356", source["revision"])
        self.assertIn("personal information", source["rights_caveat"])
        self.assertIn("third-party", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("acts and regulations", checks)
        self.assertIn("global g-0", checks)
        self.assertIn("never represent a reproduction as an official version", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 6)
        self.assertGreaterEqual(len(source["required_checks"]), 12)

    def test_world_bank_data_catalog_is_limited_to_first_party_cc_by_4_datasets(self):
        source = self.source("World Bank Data Catalog:first-party-CC-BY-4.0-only")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0"])
        self.assertIn("unless specifically labeled otherwise", source["reported_license"].casefold())
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("Microdata Research License", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("resource-level license metadata", checks)
        self.assertIn("odbl/share-alike", checks)
        self.assertIn("restricted-data list", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)
        self.assertGreaterEqual(len(source["required_checks"]), 14)


    def test_massive_11_is_text_only_cc_by_and_train_partition_candidate(self):
        source = self.source("AmazonScience/MASSIVE:1.1-text-train-only")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("f966f21846043aabef9b0f974fa7970027f43738", source["revision"])
        self.assertIn("CC BY-NC 4.0", source["reported_license"])
        self.assertIn("worker_id", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("partition is exactly train", checks)
        self.assertIn("mmnlu-22", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 6)

    def test_universal_dependencies_219_is_mixed_license_and_per_treebank_only(self):
        source = self.source("Universal Dependencies:2.19-treebanks-per-treebank-CC-BY-4.0-or-CC0-only")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0", "CC0-1.0"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("11234/1-6316", source["revision"])
        self.assertIn("Spanish AnCora", source["rights_caveat"])
        self.assertIn("GUMReddit", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("license.txt", checks)
        self.assertIn("readme", checks)
        self.assertIn("*-train.conllu", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 6)

    def test_common_voice_v27_respects_current_mdc_no_mirroring_terms(self):
        source = self.source("Mozilla Data Collective:Common Voice Scripted Speech v27.0 (text-only)")
        self.assert_discovery_only(source)
        self.assertIs(source["acquisition_enabled"], False)
        self.assertEqual(source["terms_effective_date"], "2025-10-31")
        self.assertIn("not to post", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("no posting, distribution or mirroring", checks)
        self.assertIn("commonvoice.mozilla.org/oc/terms", " ".join(source["evidence_urls"]))

    def test_global_g0_is_blocked_until_all_protected_splits_are_inventoried(self):
        gate = self.registry["global_g0_status"]
        self.assertEqual(gate["status"], "blocked_incomplete_split_inventory")
        self.assertIn("validation/test/benchmark/holdout", gate["missing_scope"])
        self.assertIn("120 synthetic", gate["missing_scope"])
        self.assertIn("not a complete global G-0", gate["reason"])

    def test_registry_source_count_matches_source_records(self):
        self.assertEqual(self.registry["source_count"], len(self.registry["sources"]))

    def test_oecd_data_explorer_is_series_level_rights_candidate_only(self):
        source = self.source("OECD:Data-Explorer-first-party-unrestricted-series")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIn("commercial", source["reported_license"])
        self.assertIn("third parties", source["reported_license"])
        self.assertIn("source tab", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("contentconstraint", checks)
        self.assertIn("60-downloads-per-hour", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 4)

    def test_statistics_canada_aggregate_data_is_open_licence_candidate_only(self):
        source = self.source("Statistics Canada:Open-Licence-aggregate-statistics-only")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIn("worldwide, royalty-free", source["reported_license"])
        self.assertIn("owner or licensee", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("public-use microdata", checks)
        self.assertIn("attempt to identify", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)


    def test_ilostat_aggregate_tables_are_discovery_only(self):
        source = self.source("ILO:ILOSTAT-post-2023-aggregate-statistics-and-dictionaries")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("2023-05-03", source["reported_license"])
        self.assertIn("microdata", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("microdata", checks)
        self.assertIn("note_source", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)


    def test_uis_data_browser_excluded_for_unapproved_sharealike(self):
        source = self.source("UNESCO UIS:Data-Browser-CC-BY-SA-4.0")
        self.assertEqual(source["status"], "excluded_unapproved_sharealike")
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-SA-4.0")
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("share-alike", source["rights_caveat"])

    def test_un_comtrade_blocked_pending_internal_use_and_redistribution_rights(self):
        source = self.source("UNSD:UN-Comtrade-internal-use-and-redistribution-restrictions")
        self.assertTrue(source["status"].startswith("blocked_internal_use"))
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("institutional unit", source["reported_license"])
        self.assertIn("AI model", source["reported_license"])
        self.assertIn("redistribute", source["rights_caveat"])

    def test_hansard_daily_reports_require_item_level_opl_and_privacy_review(self):
        source = self.source("UK Parliament:Hansard-daily-reports-explicit-OPL-v3-only")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "OPL-UK-3.0")
        self.assertEqual(source["license_exact_allowlist"], ["OPL-UK-3.0"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("daily PDF", source["reported_license"])
        self.assertIn("personal data", source["rights_caveat"])
        self.assertIn("Historic Hansard", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("exact opl-uk-3.0", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)
        self.assertGreaterEqual(len(source["required_checks"]), 12)

    def test_europeana_metadata_only_candidate_is_cc0_without_content_rights_inference(self):
        source = self.source("Europeana:multilingual-cultural-heritage-metadata-only-CC0-1.0")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC0-1.0")
        self.assertIs(source["acquisition_enabled"], False)
        self.assertEqual(source["payload_scope"], "Metadata fields only; no digital-object bytes or linked provider content.")
        self.assertIn("metadata only", source["reported_license"].casefold())
        self.assertIn("not the owner", source["rights_caveat"])
        self.assertIn("edm:rights", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("xml:lang", checks)
        self.assertIn("do not fetch", checks)
        self.assertIn("api key", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)

    def test_new_zealand_legislation_is_limited_to_section_27_works_and_pinned_versions(self):
        source = self.source("New Zealand Legislation:official-acts-bills-regulations-no-copyright-s27")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "LicenseRef-NZ-Legislation-No-Copyright-s27")
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("section 27", source["reported_license"])
        self.assertIn("incorporated by reference", source["rights_caveat"])
        self.assertIn("agency-published secondary legislation", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("version_id", checks)
        self.assertIn("10,000 requests", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 4)
        self.assertGreaterEqual(len(source["required_checks"]), 14)

    def test_latest_scheduled_acquisitions_are_verified_zero_byte_storage_blocks(self):
        last = self.registry["last_candidate_batch_details"]
        previous = self.registry["previous_candidate_batch_details"]
        self.assertEqual(last["run_id"], 45969736101)
        self.assertEqual(last["run_number"], 166)
        self.assertEqual(previous["run_id"], 45900766740)
        self.assertEqual(previous["run_number"], 165)
        self.assertEqual(last["source_group"], 1)
        self.assertEqual(previous["source_group"], 7)
        self.assertEqual(last["artifact_id"], 15184268031)
        self.assertEqual(previous["artifact_id"], 15156090956)
        self.assertEqual(last["artifact_sha256"], "5cde9471e155fc56cf5c59cfb10c6b6922aaccc625e79d7bc8a8a90e91de9f12")
        self.assertEqual(previous["artifact_sha256"], "0ca28a1224eb8f57adf481528e9dab3a93ba3850bb41eb2b31e49132dc623902")
        self.assertEqual(last["manifest_sha256"], "5a29c6d9b12146e5ba7b8e76a7a849275303a6c7e21b61ab0907fca8eb78c437")
        self.assertEqual(previous["manifest_sha256"], "3b605cda44c2b6711ea9f30d9926a2a2af9d8194edda80f6b102e51a04e16992")
        history = {batch["run_number"]: batch for batch in self.registry["historical_candidate_batches"] if batch.get("run_number") is not None}
        self.assertEqual(history[149]["artifact_id"], 14770830618)
        self.assertEqual(history[150]["artifact_id"], 14800025470)
        self.assertEqual(history[162]["artifact_id"], 15066562283)
        self.assertEqual(history[163]["artifact_id"], 15100551941)
        self.assertEqual(history[165]["artifact_id"], 15156090956)
        self.assertEqual(history[166]["artifact_id"], 15184268031)
        for batch in (last, previous):
            self.assertEqual(batch["candidate_rows"], 0)
            self.assertEqual(batch["candidate_jsonl_bytes"], 0)
            self.assertIsNone(batch["remote_bytes_announced"])
            self.assertIsNone(batch["remote_bytes_downloaded"])
            self.assertIsNone(batch["compressed_source_bytes"])
            self.assertEqual(batch["downloaded_jsonl_bytes_in_runner"], 0)
            self.assertEqual(batch["retained_payload_bytes"], 0)
            self.assertEqual(batch["admitted_bytes_added"], 0)
            self.assertIs(batch["training_authorized"], False)
            self.assertIs(batch["checks"]["payload_downloaded"], False)
            self.assertEqual(batch["storage_gate"]["status"], "blocked")
            self.assertEqual(batch["manifest_bytes"], 871)
            self.assertEqual(batch["artifact_zip_bytes"], 653)



    def test_un_parallel_corpus_v10_is_public_domain_six_language_train_only_candidate(self):
        source = self.source("United Nations:Parallel-Corpus-v1.0-public-domain-six-languages")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("no other restrictions", source["reported_license"].casefold())
        self.assertIn("2015", source["rights_caveat"])
        self.assertIn("UNv1.0.testsets.tar.gz", " ".join(source["required_checks"]))
        self.assertIn("global g-0", " ".join(source["required_checks"]).casefold())
        self.assertEqual(set(source["language"]), {"ar", "en", "es", "fr", "ru", "zh"})
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)

    def test_mot_v111_requires_first_party_voa_article_text_and_excludes_wire_content(self):
        source = self.source("BLTLab:Multilingual-Open-Text-v1.11-first-party-VOA-article-text-only")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("9204cad746dfff0921e7a8f64c0cc0917bc75554", source["revision"])
        self.assertIn("AFP", source["rights_caveat"])
        self.assertIn("Reuters", source["rights_caveat"])
        self.assertIn("article", source["payload_scope"])
        self.assertIn("43", source["language"][0])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("content-type=article", checks)
        self.assertIn("first-party", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 6)

    def test_jrc_dcep_is_blocked_for_research_only_reuse_scope(self):
        source = self.source("European Commission:JRC-DCEP-non-exclusive-research-purpose-only")
        self.assertTrue(source["status"].startswith("blocked_research_only"))
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("research purposes", source["reported_license"])

    def test_lr_sum_is_blocked_pending_research_scope_and_upstream_rights(self):
        source = self.source("BLTLab:LR-Sum-research-purpose-card-and-VOA-upstream-rights-pending")
        self.assertTrue(source["status"].startswith("blocked_research_only"))
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertIs(source["training_authorized"], False)
        self.assertIs(source["count_toward_admitted_bytes"], False)
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("primarily released for research", source["reported_license"])
        self.assertIn("AFP", source["rights_caveat"])


    def test_parallel_global_voices_requires_article_level_rights_attribution_and_privacy_review(self):
        source = self.source("CLARIN/ILSP:Parallel-Global-Voices-2015-2016")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("CC BY 3.0", source["reported_license"])
        self.assertIn("CC BY 4.0", source["reported_license"])
        self.assertIn("unless otherwise stated", source["reported_license"])
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("byline", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("original page", checks)
        self.assertIn("sentence alignment", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 5)
        self.assertGreaterEqual(len(source["required_checks"]), 12)

    def test_parlamint_v50_requires_per_parliament_rights_and_excludes_sensitive_metadata(self):
        source = self.source("CLARIN.SI:ParlaMint.ana-5.0-original-language-corpora")
        self.assert_discovery_only(source)
        self.assertEqual(source["spdx_license_identifier"], "CC-BY-4.0")
        self.assertEqual(source["license_exact_allowlist"], ["CC-BY-4.0"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("978f9051793367fc2192eedc80c1e71ac8ec7ea5", source["revision"])
        self.assertIn("11356/2006", source["rights_caveat"])
        self.assertIn("gender", source["rights_caveat"])
        self.assertIn("political-orientation", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("per country", checks)
        self.assertIn("speaker metadata", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 6)
        self.assertGreaterEqual(len(source["required_checks"]), 14)


    def test_historical_cosmopedia_audit_is_source_scoped_not_complete_global_g0(self):
        audit = self.registry["latest_global_audit"]
        self.assertEqual(audit["audit_scope"], "source_scoped_train_artifact_plus_explicit_curated_candidates")
        self.assertIs(audit["global_g0_complete"], False)
        self.assertEqual(audit["global_g0_status"], "blocked_incomplete_split_inventory")
        self.assertIs(audit["protected_split_inventory_complete"], False)
        self.assertIn("not a complete global G-0", audit["scope_warning"])
        self.assertIn("not a complete repository-wide G-0", audit["training_authorized_scope"])
        self.assertEqual(self.registry["global_g0_status"]["status"], "blocked_incomplete_split_inventory")


    def test_us_federal_register_candidate_uses_item_level_1_cfr_2_6_and_keeps_xml_quality_gates(self):
        source = self.source("US GovInfo:Federal-Register-official-edition-XML-2000-present")
        self.assert_discovery_only(source)
        self.assertIsNone(source["spdx_license_identifier"])
        self.assertIs(source["acquisition_enabled"], False)
        self.assertIn("1 CFR 2.6", source["reported_license"])
        self.assertIn("not an SPDX", source["reported_license"])
        self.assertIn("2000 onward", source["revision"])
        self.assertIn("not the official online legal format", source["payload_scope"])
        self.assertIn("third-party", source["rights_caveat"])
        self.assertIn("Library of Congress", source["rights_caveat"])
        checks = " ".join(source["required_checks"]).casefold()
        self.assertIn("sha-256", checks)
        self.assertIn("official pdf/text", checks)
        self.assertIn("external entities", checks)
        self.assertIn("global g-0", checks)
        self.assertGreaterEqual(len(source["evidence_urls"]), 6)
        self.assertGreaterEqual(len(source["required_checks"]), 15)

if __name__ == "__main__":
    unittest.main()
