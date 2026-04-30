-- 1. Top ranked opportunities.
SELECT rank, asset, category, final_score, decision, next_question
FROM market_events
ORDER BY final_score DESC
LIMIT 10;

-- 2. Category summary.
SELECT
    category,
    COUNT(*) AS event_count,
    ROUND(AVG(final_score), 1) AS average_score,
    SUM(CASE WHEN decision = 'research further' THEN 1 ELSE 0 END) AS research_now
FROM market_events
GROUP BY category
ORDER BY average_score DESC;

-- 3. High-risk watchlist.
SELECT asset, downside_risk, volatility, final_score, catalyst
FROM market_events
WHERE downside_risk >= 4 OR volatility >= 5
ORDER BY final_score DESC;

-- 4. Evidence gaps.
SELECT asset, evidence_quality, source_count, market_signal, next_question
FROM market_events
WHERE evidence_quality < 4 OR source_count < 3
ORDER BY evidence_quality ASC, source_count ASC;

-- 5. Timing-sensitive opportunities.
SELECT asset, timing_window, catalyst, final_score, decision
FROM market_events
WHERE timing_window >= 4
ORDER BY timing_window DESC, final_score DESC;
