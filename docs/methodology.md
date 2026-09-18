# Methodology

## Source

The project uses the CC0 dataset *3 million Sudoku puzzles with ratings*. Each record contains a puzzle, its solution, clue count and a continuous difficulty rating derived from average solver search-tree depth over ten attempts.

## Confirmatory tests

The thresholds below are project decision rules declared before the final dashboard was built. They are not preregistered universal standards. The analysis emphasises practical effect size rather than p-values because three million observations can make negligible effects statistically detectable.

### H1: clue-count hypothesis

- Product hypothesis: clue count has at least a weak practical association with the supplied solver rating.
- Project criterion: clue count is considered potentially useful only if Pearson or Spearman absolute correlation reaches `0.10`.
- Decision implication: results below the threshold mean clue count should not be the primary labelling rule.

### H2: surface-feature hypothesis

- Product hypothesis: basic visible structure explains enough rating variation to support classification.
- Baseline: an out-of-sample model using clue-count categories, allowing a different average rating for each observed clue count.
- Comparison: a separate out-of-sample linear model using numeric clue count plus standardised summaries of row, column, box and digit balance, rotational symmetry, minimum clues by region and basic centre, corner and edge location.
- Project criterion: `R² ≥ 0.10` is the minimum project threshold for potential usefulness.

Surface features are engineered on a deterministic random sample of 100,000 puzzles. A seeded 80/20 split fits each model on 80,000 rows and evaluates it on the same unseen 20,000-row test set. The models are separate diagnostic specifications, not a nested feature-ablation or production machine-learning system. Their purpose is to test whether either visible-metadata specification contains sufficient signal. One split is adequate for this large gap from the decision threshold, but production modelling would require repeated validation and additional technique-level features.

## Data validation

The source archive hash, row-level missingness, duplicate IDs and puzzles, string formats and reported clue counts are checked across all 3,000,000 rows. Completed solution grids and agreement between each puzzle’s givens and supplied solution are checked on a deterministic 50,000-row sample. This is a scoped source-quality audit, not proof that every puzzle has exactly one solution. The displayed 23-clue hero puzzle is checked separately and has exactly one solution matching the supplied solution.

## Exploratory questions

- How is the catalogue distributed across provisional difficulty tiers?
- Which clue counts contain the widest difficulty range?
- Which puzzles most strongly contradict the fewer-clues-equals-harder assumption?
- What telemetry would be required to measure human-perceived difficulty?

## Dashboard display scope

The correlations and grouped summaries use all 3,000,000 records; the surface-feature analysis uses the documented 100,000-row sample. The three dashboard charts display clue counts 21–28, which contain 2,999,482 records (99.98% of the catalogue). The 518 records in the sparse 19–20 and 29–31 clue tails remain in all full-population metrics but are excluded from the charts because their per-bucket estimates are unstable. The difficulty-spread chart uses the 90th-minus-10th-percentile range rather than the full minimum-to-maximum range to reduce sensitivity to isolated extremes.

## Provisional tiers

| Tier | Solver rating | Interpretation |
| --- | ---: | --- |
| Beginner | `0.0` | Solvable using the source solver's scanning method |
| Intermediate | `0.1–2.0` | Limited solver search depth |
| Advanced | `2.1–4.0` | Greater solver search depth |
| Expert | `>4.0` | Highest-complexity tail |

These analysis-defined labels are only a descriptive translation of the source metric. They are not the beginner, intermediate and advanced player segments proposed for future calibration, and they require validation against human gameplay before production use.

## AI-assisted workflow

AI was used to accelerate source discovery, code scaffolding, validation coverage, Tableau implementation and quality checks. The project owner defines the question, reviews the methodology, verifies outputs against the source and owns the interpretation. No synthetic gameplay or customer data is introduced.
