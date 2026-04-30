from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import ScoredEvent


SCHEMA = """
CREATE TABLE IF NOT EXISTS market_events (
    rank INTEGER PRIMARY KEY,
    event_id TEXT NOT NULL UNIQUE,
    asset TEXT NOT NULL,
    category TEXT NOT NULL,
    catalyst TEXT NOT NULL,
    market_signal TEXT NOT NULL,
    source_count INTEGER NOT NULL,
    evidence_quality INTEGER NOT NULL,
    volatility INTEGER NOT NULL,
    downside_risk INTEGER NOT NULL,
    timing_window INTEGER NOT NULL,
    catalyst_score REAL NOT NULL,
    evidence_score REAL NOT NULL,
    risk_score REAL NOT NULL,
    timing_score REAL NOT NULL,
    final_score REAL NOT NULL,
    decision TEXT NOT NULL,
    next_question TEXT NOT NULL,
    notes TEXT NOT NULL
);
"""


def write_sqlite(rows: list[ScoredEvent], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("DROP TABLE IF EXISTS market_events")
        conn.executescript(SCHEMA)
        conn.executemany(
            """
            INSERT INTO market_events (
                rank, event_id, asset, category, catalyst, market_signal, source_count,
                evidence_quality, volatility, downside_risk, timing_window,
                catalyst_score, evidence_score, risk_score, timing_score,
                final_score, decision, next_question, notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [_to_record(rank, row) for rank, row in enumerate(rows, start=1)],
        )


def _to_record(rank: int, row: ScoredEvent) -> tuple[object, ...]:
    event = row.event
    return (
        rank,
        event.event_id,
        event.asset,
        event.category,
        event.catalyst,
        event.market_signal,
        event.source_count,
        event.evidence_quality,
        event.volatility,
        event.downside_risk,
        event.timing_window,
        row.catalyst_score,
        row.evidence_score,
        row.risk_score,
        row.timing_score,
        row.final_score,
        row.decision,
        row.next_question,
        event.notes,
    )
