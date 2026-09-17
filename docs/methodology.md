# Methodology

## Source

The project uses the CC0 dataset *3 million Sudoku puzzles with ratings*. Each record contains a puzzle, its solution, clue count and a continuous difficulty rating derived from average solver search-tree depth over ten attempts.

## Confirmatory tests

The thresholds below are declared before the final dashboard is built.

### H1: clue-count hypothesis

- Null framing: clue count is meaningfully associated with difficulty.
- Project criterion: both Pearson and Spearman association are considered weak when their absolute values are below `0.10`.
- Decision implication: a weak result means clue count should not be the primary labelling rule.

### H2: surface-feature hypothesis

- Baseline: an out-of-sample model using clue count only.
- Comparison: an out-of-sample linear model using clue count, clue-distribution measures, symmetry and clue-position measures.
- Project criterion: `R² < 0.10` indicates that visible surface features explain too little rating variation for dependable classification.

The models are diagnostic rather than production machine-learning systems. Their purpose is to test whether visible metadata contains sufficient signal.

## Exploratory questions

- How is the catalogue distributed across provisional difficulty tiers?
- Which clue counts contain the widest difficulty range?
- Which puzzles most strongly contradict the fewer-clues-equals-harder assumption?
- What telemetry would be required to measure human-perceived difficulty?

## Dashboard display scope

The statistical analysis uses all 3,000,000 records. The three dashboard charts display clue counts 21–28, which contain 2,999,482 records (99.98% of the catalogue). The 518 records in the sparse 19–20 and 29–31 clue tails remain in all full-population metrics but are excluded from the charts because their per-bucket estimates are unstable. The difficulty-spread chart uses the 90th-minus-10th-percentile range rather than the full minimum-to-maximum range to reduce sensitivity to isolated extremes.

## Provisional tiers

| Tier | Solver rating | Interpretation |
| --- | ---: | --- |
| Beginner | `0.0` | Solvable using the source solver's scanning method |
| Intermediate | `0.1–2.0` | Limited solver search depth |
| Advanced | `2.1–4.0` | Greater solver search depth |
| Expert | `>4.0` | Highest-complexity tail |

These labels are a product-facing translation of the source metric. They require validation against human gameplay before production use.

## AI-assisted workflow

AI was used to accelerate source discovery, code scaffolding, validation coverage, Tableau implementation and quality checks. The project owner defines the question, reviews the methodology, verifies outputs against the source and owns the interpretation. No synthetic gameplay or customer data is introduced.
