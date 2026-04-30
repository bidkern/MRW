from pathlib import Path

from market_research_workflow.ingest import read_events
from market_research_workflow.scoring import score_event, score_events


def test_score_events_orders_by_final_score():
    scored = score_events(read_events(Path("sample_data/input_events.csv")))

    assert scored[0].final_score >= scored[-1].final_score
    assert scored[0].decision == "research further"


def test_high_risk_high_volatility_is_watch_only():
    event = read_events(Path("sample_data/input_events.csv"))[1]
    scored = score_event(event)

    assert scored.decision == "watch only"
    assert "invalidate" in scored.next_question


def test_scoring_is_deterministic():
    events = read_events(Path("sample_data/input_events.csv"))

    first = [row.final_score for row in score_events(events)]
    second = [row.final_score for row in score_events(events)]

    assert first == second
