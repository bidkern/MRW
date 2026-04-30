# Market Research Workflow

A public-safe Python and SQL workflow for turning raw market observations into ranked research opportunities. It validates CSV input, scores each event with transparent heuristics, exports ranked CSV output, and can load the result into SQLite for repeatable analysis.

This is a portfolio project, not financial advice. The sample data is synthetic.

## Why It Matters

Market research gets noisy quickly. This project forces every idea through the same questions:

- how strong is the catalyst?
- how credible is the evidence?
- how crowded or volatile is the setup?
- what is the downside risk?
- what would change the decision?

That makes research notes easier to compare, review, and improve over time.

## Quick Start

```bash
python score_events.py sample_data/input_events.csv
```

The command writes:

- `outputs/ranked_events.csv`
- `outputs/decision_log.csv`
- `outputs/research.db`

Run the tests:

```bash
python -m pytest
```

The project uses only the Python standard library at runtime. `pytest` is only needed for tests.

## Example Output

```text
score decision          event_id asset
 86.0 research further  MKT-001  Regional Grocery Basket
 82.0 research further  MKT-009  Cybersecurity Midcap Index
 78.0 research further  MKT-017  Discount Retail Basket
```

## Project Structure

```text
.
|-- README.md
|-- LICENSE
|-- score_events.py
|-- requirements.txt
|-- .gitignore
|-- examples/
|-- sample_data/input_events.csv
|-- src/market_research_workflow/
|   |-- database.py
|   |-- exports.py
|   |-- ingest.py
|   |-- models.py
|   `-- scoring.py
|-- sql/analysis_queries.sql
`-- tests/
```

## Scoring Model

Each event receives four component scores:

- `catalyst_score`: urgency and clarity of the market change
- `evidence_score`: quality of supporting observations
- `risk_score`: inverted downside risk, so lower risk scores better
- `timing_score`: usefulness of the opportunity window

The final score is a weighted blend:

```text
final = catalyst * 0.35 + evidence * 0.25 + risk * 0.20 + timing * 0.20
```

The workflow then assigns an action:

- `research further`: strong enough to investigate now
- `watchlist`: promising, but missing confirmation
- `hold for more evidence`: not enough support yet
- `watch only`: too much risk or volatility for the current evidence

## SQLite Analysis

`outputs/research.db` includes a normalized `market_events` table. The SQL file contains five reviewer-friendly queries:

1. top ranked opportunities
2. category summary
3. high-risk watchlist
4. evidence gaps
5. timing-sensitive opportunities

Example:

```bash
sqlite3 outputs/research.db < sql/analysis_queries.sql
```

## Design Choices

- No external runtime dependencies, so the workflow is easy to inspect and run.
- Validation fails early with row-level error messages.
- All sample events are synthetic and safe for a public repo.
- Outputs are deterministic, which makes tests and reviews straightforward.
- SQLite export makes the workflow useful beyond a one-off CSV script.

## Disclaimer

This project is a research-organization demo. It is not investment advice and does not recommend buying or selling any asset.
