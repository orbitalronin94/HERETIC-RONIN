"""Safe serialization and atomic publication for streamed candidate shards."""
from __future__ import annotations

from datetime import date, datetime
from pathlib import Path
from typing import IO


class AtomicCandidateWriter:
    """Write to a temporary path and remove it if the producer raises."""

    def __init__(self, temporary_path: Path):
        self.temporary_path = Path(temporary_path)
        self.handle: IO[str] | None = None

    def __enter__(self) -> IO[str]:
        self.temporary_path.parent.mkdir(parents=True, exist_ok=True)
        self.handle = self.temporary_path.open("w", encoding="utf-8")
        return self.handle

    def __exit__(self, exc_type, exc, traceback) -> bool:
        if self.handle is not None:
            self.handle.close()
        if exc_type is not None:
            self.temporary_path.unlink(missing_ok=True)
        return False


def finalize_candidate_file(
    temporary_path: Path,
    target_path: Path,
    rows_written: int,
    minimum_rows: int,
    source_id: str,
) -> None:
    """Publish a shard only after its minimum-row check passes."""
    temporary_path = Path(temporary_path)
    target_path = Path(target_path)
    if rows_written < minimum_rows:
        temporary_path.unlink(missing_ok=True)
        raise RuntimeError(
            f"{source_id}: only {rows_written} usable rows "
            f"(minimum {minimum_rows}); partial shard discarded"
        )
    target_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_path.replace(target_path)


def json_default(value: object) -> str:
    """Serialize date/time values in ISO-8601 form; reject unknown objects."""
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        return str(isoformat())
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


def select_source_group(sources, group_index: int, group_count: int):
    """Partition a fixed source list into deterministic, disjoint acquisition groups."""
    if group_count < 1:
        raise ValueError("group_count must be at least 1")
    if group_index < 0 or group_index >= group_count:
        raise ValueError("group_index must be within [0, group_count)")
    return [
        (index, source)
        for index, source in enumerate(sources)
        if index % group_count == group_index
    ]


def scheduled_source_group(
    day_of_year: int,
    tranche_slot: int,
    group_count: int,
    slots_per_day: int = 4,
) -> int:
    """Map each scheduled daily slot to a balanced deterministic source group.

    With four slots per day and eight groups, every consecutive 48-hour window
    visits each group exactly once. The mapping is independent of workflow run
    numbers and pull-request events.
    """
    if group_count < 1:
        raise ValueError("group_count must be at least 1")
    if slots_per_day < 1:
        raise ValueError("slots_per_day must be at least 1")
    if day_of_year < 1 or day_of_year > 366:
        raise ValueError("day_of_year must be within [1, 366]")
    if tranche_slot < 0 or tranche_slot >= slots_per_day:
        raise ValueError("tranche_slot must be within [0, slots_per_day)")
    absolute_slot = (day_of_year - 1) * slots_per_day + tranche_slot
    return absolute_slot % group_count
