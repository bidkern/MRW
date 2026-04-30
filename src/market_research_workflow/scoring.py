from __future__ import annotations

from .models import MarketEvent, ScoredEvent


def score_events(events: list[MarketEvent]) -> list[ScoredEvent]:
    rows = [score_event(event) for event in events]
    return sorted(rows, key=lambda row: (row.final_score, row.event.source_count), reverse=True)


def score_event(event: MarketEvent) -> ScoredEvent:
    catalyst_score = min(100.0, event.evidence_quality * 14 + event.source_count * 4 + _signal_bonus(event))
    evidence_score = min(100.0, event.evidence_quality * 16 + min(event.source_count, 6) * 5)
    risk_score = max(0.0, 100.0 - event.downside_risk * 16 - max(0, event.volatility - 3) * 8)
    timing_score = min(100.0, event.timing_window * 16 + (10 if event.volatility <= 3 else 0))
    final_score = round(
        catalyst_score * 0.35 + evidence_score * 0.25 + risk_score * 0.20 + timing_score * 0.20,
        1,
    )

    decision = _decision(final_score, event)
    return ScoredEvent(
        event=event,
        catalyst_score=round(catalyst_score, 1),
        evidence_score=round(evidence_score, 1),
        risk_score=round(risk_score, 1),
        timing_score=round(timing_score, 1),
        final_score=final_score,
        decision=decision,
        next_question=_next_question(event, decision),
    )


def _signal_bonus(event: MarketEvent) -> int:
    signal = event.market_signal.lower()
    if "confirmed" in signal or "multi-source" in signal:
        return 14
    if "early" in signal or "divergence" in signal:
        return 8
    if "rumor" in signal or "thin" in signal:
        return -8
    return 4


def _decision(final_score: float, event: MarketEvent) -> str:
    if event.downside_risk >= 5 and event.volatility >= 4:
        return "watch only"
    if final_score >= 75 and event.evidence_quality >= 4:
        return "research further"
    if final_score >= 60:
        return "watchlist"
    return "hold for more evidence"


def _next_question(event: MarketEvent, decision: str) -> str:
    if decision == "watch only":
        return "What downside trigger would invalidate the idea fastest?"
    if event.evidence_quality < 4:
        return "What independent evidence would raise confidence?"
    if event.downside_risk >= 4:
        return "What risk control or invalidation level matters most?"
    if event.timing_window <= 2:
        return "What near-term catalyst would make this actionable?"
    return "What metric should be tracked next?"
