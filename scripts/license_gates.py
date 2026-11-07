"""Conservative, exact matching for per-record dataset license metadata."""

from __future__ import annotations

import re


def _normalise(value: object, *, uri: bool = False) -> str:
    result = str(value).strip().casefold()
    return result.rstrip("/") if uri else result


_CC_URI = re.compile(
    r"https?://creativecommons\.org/(?:licenses/[a-z0-9-]+/[0-9.]+|publicdomain/zero/[0-9.]+)"
)
_CC_DESCRIPTOR = re.compile(
    r"(?P<label>.+?)\s+-\s+(?P<uri>https?://creativecommons\.org/"
    r"(?:licenses/[a-z0-9-]+/[0-9.]+|publicdomain/zero/[0-9.]+)/?)",
    re.IGNORECASE,
)
_CC_LABEL_BY_PATH = {
    "/licenses/by/4.0": "creative commons - attribution",
    "/licenses/by-sa/4.0": "creative commons - attribution share-alike",
    "/licenses/by-nc/4.0": "creative commons - attribution noncommercial",
    "/licenses/by-nd/4.0": "creative commons - attribution no derivatives",
    "/licenses/by-nc-sa/4.0": "creative commons - attribution noncommercial share-alike",
    "/licenses/by-nc-nd/4.0": "creative commons - attribution noncommercial no derivatives",
    "/publicdomain/zero/1.0": "creative commons zero - public domain",
}


def _canonical_cc_uri(value: object) -> str | None:
    """Return an exact CC URI, accepting only known label+URI descriptors."""
    text = str(value).strip()
    normalised = _normalise(text, uri=True)
    if _CC_URI.fullmatch(normalised):
        return normalised

    match = _CC_DESCRIPTOR.fullmatch(text)
    if not match:
        return None
    uri = _normalise(match.group("uri"), uri=True)
    path = uri.split("creativecommons.org", 1)[1]
    label = " ".join(match.group("label").casefold().split())
    if _CC_LABEL_BY_PATH.get(path) != label:
        return None
    return uri


def license_values_allowed(raw_license: object, source: dict) -> bool:
    """Return whether every declared per-record license satisfies all configured allowlists.

    Missing, empty, combined, mixed, or malformed values fail closed. Common Pile's
    documented Creative Commons label+URI descriptors are accepted only when the
    label and exact canonical URI agree. Sources without a per-record allowlist are
    unchanged and must still pass their other gates.
    """
    uri_allowlist = source.get("license_filter") or []
    name_allowlist = source.get("license_name_filter") or []
    exact_allowlist = source.get("license_exact_allowlist") or []
    all_exact_allowlist = source.get("license_all_exact_allowlist") or []

    if not any((uri_allowlist, name_allowlist, exact_allowlist, all_exact_allowlist)):
        return True

    raw_values = list(raw_license) if isinstance(raw_license, (list, tuple, set)) else [raw_license]
    if not raw_values or any(value is None or not str(value).strip() for value in raw_values):
        return False

    def all_in(allowed: list, *, uri: bool = False) -> bool:
        normalised_allowed = {
            _normalise(item, uri=uri)
            for item in allowed
            if item is not None and str(item).strip()
        }
        if not normalised_allowed:
            return False
        if uri:
            normalised_values = [_canonical_cc_uri(value) for value in raw_values]
            return all(value is not None and value in normalised_allowed for value in normalised_values)
        normalised_values = [_normalise(value) for value in raw_values]
        return all(value in normalised_allowed for value in normalised_values)

    if uri_allowlist and not all_in(uri_allowlist, uri=True):
        return False
    if name_allowlist and not all_in(name_allowlist):
        return False
    if exact_allowlist and not all_in(exact_allowlist):
        return False
    if all_exact_allowlist and not all_in(all_exact_allowlist):
        return False
    return True
