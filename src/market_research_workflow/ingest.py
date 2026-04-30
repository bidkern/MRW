from __future__ import annotations

import csv
from pathlib import Path

from .models import MarketEvent


REQUIRED_COLUMNS = {
    "event_id",
    "asset",
    "category",
    "catalyst",
    "evidence_quality",
    "volatility",
    "downside_risk",
    "timing_window",
    "market_signal",
    "source_count",
    "notes",
}


def read_events(path: Path) -> list[MarketEvent]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        missing = REQUIRED_COLUMNS.difference(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
        return [_event_from_row(row, index) for index, row in enumerate(reader, start=2)]


def _event_from_row(row: dict[str, str], row_number: int) -> MarketEvent:
    return MarketEvent(
        event_id=_required(row, "event_id", row_number),
        asset=_required(row, "asset", row_number),
        category=_required(row, "category", row_number),
        catalyst=_required(row, "catalyst", row_number),
        evidence_quality=_scale(row, "evidence_quality", row_number),
        volatility=_scale(row, "volatility", row_number),
        downside_risk=_scale(row, "downside_risk", row_number),
        timing_window=_scale(row, "timing_window", row_number),
        market_signal=_required(row, "market_signal", row_number),
        source_count=_positive_int(row, "source_count", row_number),
        notes=_required(row, "notes", row_number),
    )


def _required(row: dict[str, str], column: str, row_number: int) -> str:
    value = (row.get(column) or "").strip()
    if not value:
        raise ValueError(f"Row {row_number}: {column} is required")
    return value


def _scale(row: dict[str, str], column: str, row_number: int) -> int:
    value = _positive_int(row, column, row_number)
    if value < 1 or value > 5:
        raise ValueError(f"Row {row_number}: {column} must be between 1 and 5")
    return value


def _positive_int(row: dict[str, str], column: str, row_number: int) -> int:
    raw = _required(row, column, row_number)
    try:
        value = int(raw)
    except ValueError as exc:
        raise ValueError(f"Row {row_number}: {column} must be an integer") from exc
    if value < 0:
        raise ValueError(f"Row {row_number}: {column} must be non-negative")
    return value
