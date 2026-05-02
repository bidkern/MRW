# Portfolio Overview: MRW

MRW is a Python and SQL workflow for turning messy market observations into ranked, reviewable decisions. It is built as a portfolio project for analyst, business analyst, operations analyst, revenue operations, sales operations, customer insights, and implementation-support roles.

## What this project proves

- Can take vague business inputs and turn them into a structured scoring process.
- Can write readable Python that validates data, produces deterministic output, and supports tests.
- Can use SQL and SQLite to make the output inspectable after the script runs.
- Can document the business problem, method, and tradeoffs clearly enough for review.
- Can build public-safe sample data without exposing private information.

## Reviewer path

1. Read the case study in [README.md](README.md).
2. Run `python score_events.py sample_data/input_events.csv`.
3. Open `outputs/ranked_events.csv` and `outputs/decision_log.csv`.
4. Review `sql/analysis_queries.sql` for the analysis layer.
5. Run `python -m pytest` to verify the workflow.

## Role fit

This project is strongest evidence for roles where the work is to clean up messy inputs, create a repeatable decision process, and explain the result to non-technical stakeholders.

The value is practical analytics, operations thinking, clean documentation, and follow-through.

