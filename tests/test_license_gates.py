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


if __name__ == "__main__":
    unittest.main()
