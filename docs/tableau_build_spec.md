# Tableau dashboard specification

## Difficulty audit

Audience: Sudoku product manager or puzzle-content lead.

Decision: determine whether clue count is dependable enough to serve as the primary difficulty label.

## Layout

- Title: `Auditing Sudoku Difficulty`
- Subtitle: `Are clue counts enough to label three million puzzles?`
- KPI row: 3.0M validated puzzles, 0.035 clue–rating correlation, 43.1% scanning-only share and 2.2% expert-rated share.
- Main view: central 80% difficulty spread (`P90 − P10`) by clue count.
- Supporting view: catalogue volume by clue count.
- Supporting view: scanning-only share by clue count.
- Decision callout: clue count should remain a descriptive feature, not the primary difficulty label.
- Interpretation guardrail: source ratings measure automated-solver behaviour, not observed human difficulty.

All charts display clue counts 21–28, covering 99.98% of the catalogue. Full-population KPIs and tests use all 3,000,000 records.

## Visual system

- Canvas: 1,100 × 720 desktop layout.
- Background: white.
- Primary: deep navy.
- Accent: Tableau blue.
- Direct labels replace unnecessary legends.
- No decorative icons, maps, gauges, 3-D charts or gratuitous interactions.

## Required takeaway

Clue count does not separate difficulty consistently. Use solver-technique or solver-effort signals for initial labels, then calibrate them with player completion time, hint use, mistakes and abandonment.
