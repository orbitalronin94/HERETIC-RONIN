#!/usr/bin/env python3
"""Produce deterministic private review samples stratified by source/domain/language/format."""
from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

ROOT = Path("staging/open-source-candidates")
OUT = ROOT / "MANUAL-SAMPLE-REVIEW.json"
SEED = 20261107
PER_SOURCE = 6
PER_STRATUM = 2
MAX_STRATA_PER_SOURCE = 64
MAX_CHARS = 700
DIMENSIONS = ("domain", "language", "format")
SAFE_METADATA_FIELDS = {
    "domain", "language", "language_code", "format", "file_format",
    "mime_type", "content_type", "collection", "subset", "license",
    "url", "date", "publication_date", "jurisdiction", "court",
    "citation", "annotation_type", "word_count", "token_count", "subject",
}


def _label(value: object) -> str:
    """Convert a metadata value to a bounded, stable label."""
    if value is None:
        return "unknown"
    if isinstance(value, dict):
        for key in ("code", "name", "label", "value"):
            if value.get(key) is not None:
                return _label(value[key])
        return "unknown"
    if isinstance(value, (list, tuple, set)):
        labels = sorted({_label(item) for item in value})
        labels = [item for item in labels if item != "unknown"]
        return "|".join(labels)[:100] if labels else "unknown"
    text = " ".join(str(value).split())
    return text[:100] if text else "unknown"


def _field(row: dict, metadata: dict, keys: tuple[str, ...]) -> str:
    for key in keys:
        for container in (row, metadata):
            if key in container:
                value = _label(container[key])
                if value != "unknown":
                    return value
    return "unknown"


def _dimensions(row: dict) -> dict[str, str]:
    metadata = row.get("source_metadata")
    if not isinstance(metadata, dict):
        metadata = {}
    return {
        "source": _label(row.get("source")),
        "domain": _field(row, metadata, ("domain", "subject", "collection", "subset")),
        "language": _field(row, metadata, ("language", "language_code", "lang")),
        "format": _field(row, metadata, ("format", "file_format", "mime_type", "content_type")),
    }


def _safe_metadata(row: dict) -> dict:
    metadata = row.get("source_metadata")
    if not isinstance(metadata, dict):
        return {}
    safe = {}
    for key in sorted(SAFE_METADATA_FIELDS):
        if key in metadata and metadata[key] is not None:
            value = metadata[key]
            if isinstance(value, str):
                safe[key] = " ".join(value.split())[:300]
            elif isinstance(value, (int, float, bool)):
                safe[key] = value
            else:
                safe[key] = _label(value)
    return safe


def _seed_for(*parts: str) -> int:
    raw = "\0".join((str(SEED), *(str(part) for part in parts)))
    return int(hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16], 16)


def _priority(source: str, stratum: tuple[str, str, str]) -> str:
    return hashlib.sha256(
        "\0".join((str(SEED), source, *stratum)).encode("utf-8")
    ).hexdigest()


def _iter_rows(path: Path):
    with path.open("r", encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, start=1):
            if not line.strip():
                continue
            row = json.loads(line)
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: expected a JSON object")
            yield row


def _select_strata(source: str, stats: dict) -> set[tuple[str, str, str]]:
    """Select bounded deterministic strata while covering all four audit dimensions."""
    strata = stats["strata"]
    if len(strata) <= MAX_STRATA_PER_SOURCE:
        return set(strata)

    selected = set()
    quota = max(1, MAX_STRATA_PER_SOURCE // len(DIMENSIONS))
    for dimension_index, dimension in enumerate(DIMENSIONS):
        values = sorted(
            stats["values"][dimension],
            key=lambda value: hashlib.sha256(
                f"{SEED}\0{source}\0{dimension}\0{value}".encode("utf-8")
            ).hexdigest(),
        )
        for value in values[:quota]:
            candidates = [item for item in strata if item[dimension_index] == value]
            if candidates:
                selected.add(min(candidates, key=lambda item: _priority(source, item)))

    for item in sorted(strata, key=lambda value: _priority(source, value)):
        if len(selected) >= MAX_STRATA_PER_SOURCE:
            break
        selected.add(item)
    return selected


def _reservoir_add(bucket: list, seen: int, item: dict, limit: int, rng: random.Random) -> None:
    if len(bucket) < limit:
        bucket.append(item)
        return
    index = rng.randrange(seen)
    if index < limit:
        bucket[index] = item


def _sample_item(row: dict, dimensions: dict[str, str]) -> dict:
    text = str(row.get("text", "")).strip()
    return {
        "source": dimensions["source"],
        "revision": row.get("revision"),
        "config": row.get("config"),
        "license": row.get("license"),
        "source_metadata": _safe_metadata(row),
        "stratum": {
            "domain": dimensions["domain"],
            "language": dimensions["language"],
            "format": dimensions["format"],
        },
        "sample_basis": [],
        "text": text[:MAX_CHARS],
    }


def _sample_key(item: dict) -> str:
    stable = {
        "source": item["source"],
        "revision": item.get("revision"),
        "config": item.get("config"),
        "license": item.get("license"),
        "stratum": item["stratum"],
        "text": item["text"],
    }
    return hashlib.sha256(
        json.dumps(stable, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def _merge_samples(source_items: list, stratum_items: list) -> list:
    merged = {}
    for basis, items in (("source", source_items), ("domain_language_format", stratum_items)):
        for item in items:
            key = _sample_key(item)
            if key not in merged:
                copied = dict(item)
                copied["sample_basis"] = []
                merged[key] = copied
            if basis not in merged[key]["sample_basis"]:
                merged[key]["sample_basis"].append(basis)
    for item in merged.values():
        item["sample_basis"].sort()
    return [merged[key] for key in sorted(merged)]


def _coverage(stats: dict, selected: set[tuple[str, str, str]]) -> dict:
    result = {}
    for index, dimension in enumerate(DIMENSIONS):
        sampled_values = sorted({item[index] for item in selected})
        result[dimension] = {
            "observed_values": len(stats["values"][dimension]),
            "sampled_values": len(sampled_values),
            "values": sampled_values,
        }
    return result


def _review_file(path: Path) -> tuple[list[dict], list[dict]]:
    stats_by_source = {}
    for row in _iter_rows(path):
        dimensions = _dimensions(row)
        source = dimensions["source"]
        stats = stats_by_source.setdefault(source, {
            "rows": 0,
            "sampleable_rows": 0,
            "strata": set(),
            "values": {dimension: set() for dimension in DIMENSIONS},
        })
        stats["rows"] += 1
        text = str(row.get("text", "")).strip()
        if not text:
            continue
        stats["sampleable_rows"] += 1
        stratum = tuple(dimensions[dimension] for dimension in DIMENSIONS)
        stats["strata"].add(stratum)
        for dimension in DIMENSIONS:
            stats["values"][dimension].add(dimensions[dimension])

    selected_by_source = {
        source: _select_strata(source, stats)
        for source, stats in stats_by_source.items()
    }
    source_reservoirs = defaultdict(list)
    source_counts = defaultdict(int)
    source_rngs = {}
    stratum_reservoirs = defaultdict(list)
    stratum_counts = defaultdict(int)
    stratum_rngs = {}

    for row in _iter_rows(path):
        dimensions = _dimensions(row)
        source = dimensions["source"]
        text = str(row.get("text", "")).strip()
        if not text:
            continue
        item = _sample_item(row, dimensions)
        source_counts[source] += 1
        source_rngs.setdefault(source, random.Random(_seed_for(source, "source")))
        _reservoir_add(
            source_reservoirs[source], source_counts[source], item, PER_SOURCE, source_rngs[source]
        )

        stratum = tuple(dimensions[dimension] for dimension in DIMENSIONS)
        if stratum not in selected_by_source.get(source, set()):
            continue
        key = (source, *stratum)
        stratum_counts[key] += 1
        stratum_rngs.setdefault(key, random.Random(_seed_for(*key)))
        _reservoir_add(
            stratum_reservoirs[key], stratum_counts[key], item, PER_STRATUM, stratum_rngs[key]
        )

    reports = []
    summaries = []
    for source in sorted(stats_by_source):
        stats = stats_by_source[source]
        selected = selected_by_source[source]
        source_items = source_reservoirs[source]
        stratum_items = []
        for stratum in sorted(selected):
            stratum_items.extend(stratum_reservoirs[(source, *stratum)])
        samples = _merge_samples(source_items, stratum_items)
        coverage = _coverage(stats, selected)
        reports.append({
            "file": path.name,
            "source": source,
            "rows": stats["rows"],
            "sampleable_rows": stats["sampleable_rows"],
            "strata_observed": len(stats["strata"]),
            "strata_sampled": len(selected),
            "coverage": coverage,
            "samples": samples,
        })
        summaries.append({
            "file": path.name,
            "source": source,
            "rows": stats["rows"],
            "sampleable_rows": stats["sampleable_rows"],
            "sample_count": len(samples),
            "strata_observed": len(stats["strata"]),
            "strata_sampled": len(selected),
            "coverage": coverage,
        })
    return reports, summaries


def main():
    reports = []
    summaries = []
    for path in sorted(ROOT.glob("*.jsonl")):
        file_reports, file_summaries = _review_file(path)
        reports.extend(file_reports)
        summaries.extend(file_summaries)

    OUT.write_text(
        json.dumps({
            "schema": "heretic-manual-sample-review-v2",
            "seed": SEED,
            "stratification": ["source", "domain", "language", "format"],
            "samples_per_source": PER_SOURCE,
            "samples_per_selected_stratum": PER_STRATUM,
            "max_strata_per_source": MAX_STRATA_PER_SOURCE,
            "text_chars_per_sample": MAX_CHARS,
            "sources": reports,
        }, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    summary = {
        "schema": "heretic-manual-sample-review-v2",
        "seed": SEED,
        "stratification": ["source", "domain", "language", "format"],
        "sources": summaries,
        "total_sample_count": sum(item["sample_count"] for item in summaries),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
