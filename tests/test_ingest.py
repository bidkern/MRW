from pathlib import Path

import pytest

from market_research_workflow.ingest import read_events


def test_read_events_loads_sample_data():
    events = read_events(Path("sample_data/input_events.csv"))

    assert len(events) == 24
    assert events[0].event_id == "MKT-001"
    assert events[0].evidence_quality == 5


def test_read_events_rejects_missing_required_columns(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text("event_id,asset\nMKT-999,Example\n", encoding="utf-8")

    with pytest.raises(ValueError, match="Missing required columns"):
        read_events(bad_csv)


def test_read_events_rejects_out_of_range_scale(tmp_path):
    bad_csv = tmp_path / "bad.csv"
    bad_csv.write_text(
        "event_id,asset,category,catalyst,evidence_quality,volatility,downside_risk,timing_window,market_signal,source_count,notes\n"
        "MKT-999,Example,Test,Signal,6,2,1,3,confirmed,2,Note\n",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="evidence_quality must be between 1 and 5"):
        read_events(bad_csv)
