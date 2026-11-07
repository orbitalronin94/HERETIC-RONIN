"""Conservative, exact matching for per-record dataset license metadata."""

from __future__ import annotations


def _normalise(value: object, *, uri: bool = False) -> str:
    result = str(value).strip().casefold()
    return result.rstrip("/") if uri else result


def license_values_allowed(raw_license: object, source: dict) -> bool:
    """Return whether every declared per-record license satisfies all configured allowlists.

    Missing, empty, combined, or mixed allowlist values fail closed. Sources without
    a per-record allowlist are unchanged and must still pass their other gates.
    """
    uri_allowlist = source.get("license_filter") or []
    name_allowlist = source.get("license_name_filter") or []
    exact_allowlist = source.get("license_exact_allowlist") or []
    all_exact_allowlist = source.get("license_all_exact_allowlist") or []

    if not any((uri_allowlist, name_allowlist, exact_allowlist, all_exact_allowlist)):
        return True

    raw_values = raw_license if isinstance(raw_license, (list, tuple, set)) else [raw_license]
    values = [_normalise(value) for value in raw_values if value is not None and str(value).strip()]
    if not values:
        return False

    def all_in(allowed: list, *, uri: bool = False) -> bool:
        normalised_allowed = {_normalise(item, uri=uri) for item in allowed if item is not None and str(item).strip()}
        if not normalised_allowed:
            return False
        normalised_values = [_normalise(value, uri=uri) for value in raw_values if value is not None and str(value).strip()]
        return bool(normalised_values) and all(value in normalised_allowed for value in normalised_values)

    if uri_allowlist and not all_in(uri_allowlist, uri=True):
        return False
    if name_allowlist and not all_in(name_allowlist):
        return False
    if exact_allowlist and not all_in(exact_allowlist):
        return False
    if all_exact_allowlist and not all_in(all_exact_allowlist):
        return False
    return True
