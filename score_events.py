from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from market_research_workflow.database import write_sqlite
from market_research_workflow.exports import write_decision_log, write_ranked_events
from market_research_workflow.ingest import read_events
from market_research_workflow.scoring import score_events


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Score and rank public-safe market research events.")
    parser.add_argument("input_csv", help="CSV file containing market events to score.")
    parser.add_argument("--output-dir", default="outputs", help="Directory for CSV and SQLite outputs.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    scored = score_events(read_events(Path(args.input_csv)))

    ranked_path = output_dir / "ranked_events.csv"
    decision_path = output_dir / "decision_log.csv"
    database_path = output_dir / "research.db"

    write_ranked_events(scored, ranked_path)
    write_decision_log(scored, decision_path)
    write_sqlite(scored, database_path)

    print("score decision          event_id asset")
    for row in scored[:10]:
        print(f"{row.final_score:>5.1f} {row.decision:<17} {row.event.event_id:<8} {row.event.asset}")
    print()
    print(f"Wrote {ranked_path}")
    print(f"Wrote {decision_path}")
    print(f"Wrote {database_path}")


if __name__ == "__main__":
    main()
