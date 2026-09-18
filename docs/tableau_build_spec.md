# Tableau dashboard specification

## Difficulty audit

Audience: Sudoku product manager or puzzle-content lead.

Decision: determine whether clue count is dependable enough to serve as the primary difficulty label.

## Layout

- Title: `Auditing Sudoku Difficulty`
- Subtitle: `Are clue counts enough to label three million puzzles?`
- KPI row: 3.0M records analysed, 0.035 clue–rating correlation, 43.1% scanning-only share and 2.2% with a rating above 4.0. The last KPI is an analysis-defined provisional tail, not a validated human Expert category.
- Main view: central 80% difficulty spread (`P90 − P10`) by clue count.
- Supporting view: catalogue volume by clue count.
- Supporting view: scanning-only share by clue count.
- Decision callout: clue count should remain a descriptive feature, not the primary difficulty label.
- Interpretation guardrail: source ratings measure automated-solver behaviour, not observed human difficulty.

All charts display clue counts 21–28, covering 99.98% of the catalogue. Full-population KPIs, correlations and grouped summaries use all 3,000,000 records; the surface-feature model uses the documented 100,000-row sample.

## Visual system

- Canvas: 1,100 × 720 desktop layout.
- Background: white.
- Primary: deep navy.
- Accent: Tableau blue.
- Direct labels replace unnecessary legends.
- No decorative icons, maps, gauges, 3-D charts or gratuitous interactions.

## Required takeaway

Clue count does not separate the supplied solver rating consistently. Use solver complexity only for provisional cold-start labels. Once enough gameplay exists, let completion time, hints, mistakes, restarts and abandonment determine player-facing labels within demonstrated skill groups.
