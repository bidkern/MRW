from __future__ import annotations

import csv
from pathlib import Path

from .models import ScoredEvent


RANKED_FIELDS = [
    "rank",
    "event_id",
    "asset",
    "category",
    "final_score",
    "decision",
    "catalyst_score",
    "evidence_score",
    "risk_score",
    "timing_score",
    "catalyst",
    "market_signal",
    "next_question",
    "notes",
]


def write_ranked_events(rows: list[ScoredEvent], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RANKED_FIELDS)
        writer.writeheader()
        for rank, row in enumerate(rows, start=1):
            writer.writerow(_ranked_row(rank, row))


def write_decision_log(rows: list[ScoredEvent], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["event_id", "asset", "decision", "next_question"])
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "event_id": row.event.event_id,
                    "asset": row.event.asset,
                    "decision": row.decision,
                    "next_question": row.next_question,
                }
            )


def _ranked_row(rank: int, row: ScoredEvent) -> dict[str, str | int | float]:
    event = row.event
    return {
        "rank": rank,
        "event_id": event.event_id,
        "asset": event.asset,
        "category": event.category,
        "final_score": row.final_score,
        "decision": row.decision,
        "catalyst_score": row.catalyst_score,
        "evidence_score": row.evidence_score,
        "risk_score": row.risk_score,
        "timing_score": row.timing_score,
        "catalyst": event.catalyst,
        "market_signal": event.market_signal,
        "next_question": row.next_question,
        "notes": event.notes,
    }
