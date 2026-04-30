import csv
import sqlite3
import subprocess
import sys


def test_cli_writes_ranked_csv_and_sqlite(tmp_path):
    output_dir = tmp_path / "outputs"
    result = subprocess.run(
        [
            sys.executable,
            "score_events.py",
            "sample_data/input_events.csv",
            "--output-dir",
            str(output_dir),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Wrote" in result.stdout
    ranked_path = output_dir / "ranked_events.csv"
    decision_path = output_dir / "decision_log.csv"
    database_path = output_dir / "research.db"
    assert ranked_path.exists()
    assert decision_path.exists()
    assert database_path.exists()

    with ranked_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 24
    assert rows[0]["decision"] == "research further"

    with sqlite3.connect(database_path) as conn:
        count = conn.execute("SELECT COUNT(*) FROM market_events").fetchone()[0]
    assert count == 24
