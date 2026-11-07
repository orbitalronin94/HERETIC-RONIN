import unittest

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

    def test_unknown_and_missing_license_fail_closed(self):
        allowed = {"license_filter": ["https://creativecommons.org/licenses/by/4.0/"]}
        self.assertFalse(license_values_allowed(None, allowed))
        self.assertFalse(license_values_allowed("", allowed))
        self.assertFalse(license_values_allowed("unknown", allowed))

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


if __name__ == "__main__":
    unittest.main()
