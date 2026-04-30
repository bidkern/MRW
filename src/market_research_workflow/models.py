from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketEvent:
    event_id: str
    asset: str
    category: str
    catalyst: str
    evidence_quality: int
    volatility: int
    downside_risk: int
    timing_window: int
    market_signal: str
    source_count: int
    notes: str


@dataclass(frozen=True)
class ScoredEvent:
    event: MarketEvent
    catalyst_score: float
    evidence_score: float
    risk_score: float
    timing_score: float
    final_score: float
    decision: str
    next_question: str
