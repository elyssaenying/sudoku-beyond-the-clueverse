# Findings

## Hypothesis results

### H1: clue count is practically useful — not supported

- Pearson correlation: `0.0353`
- Spearman correlation: `0.0409`
- Project usefulness threshold: absolute correlation of at least `0.10`

Clue count does not provide a useful ordering of the supplied solver rating. The direction is slightly positive in this generated catalogue, contradicting the common assumption that fewer clues automatically means a harder puzzle. With three million rows this small association may be statistically detectable, but its magnitude is too small to support the product decision.

### H2: visible surface features support dependable classification — not supported

Performance on a deterministic 20,000-row test set:

| Model | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Clue count only | 1.0882 | 1.2705 | 0.0012 |
| Visible surface features | 1.0840 | 1.2668 | 0.0069 |

These are separate diagnostic specifications rather than a nested incremental test. The clue-only model uses clue-count categories. The surface model uses clue count plus standardised summaries of distribution, basic location, balance and symmetry. Both remain far below the project’s `R² ≥ 0.10` usefulness threshold, so the absolute conclusion does not depend on treating the difference between them as a causal improvement.

## Exploratory findings

- `43.1%` of the catalogue has a rating of `0.0`, meaning the source solver can complete those puzzles using its scanning method.
- Only `2.2%` of puzzles have a source rating above `4.0`; the project calls this the provisional Expert tier, not a validated human-skill category.
- Puzzles with 23 clues span the entire observed rating range, from `0.0` to `8.5`.
- Puzzles with 24 clues also span almost the full range, from `0.0` to `8.2`.
- No individual visible feature in the 100,000-puzzle sample has an absolute Pearson correlation above `0.05` with difficulty.

## Product recommendation

Use solver complexity to give new puzzles a provisional difficulty tier, but let observed player behaviour become the primary evidence once enough data is available. Measure completion time, hints, mistakes, restarts and abandonment separately across demonstrated skill levels, then provide skill-calibrated labels. If one catalogue-wide label is required, combine group-level results using transparent weights that reflect the product’s player base.

## Evidence boundary

The source rating reflects automated solver search-tree depth. It is not a direct measurement of human-perceived difficulty, enjoyment, engagement or retention. The surface model tests summary features rather than every exact clue arrangement or named solving technique. The project supports a provisional catalogue-classification decision and a human-data measurement plan; it does not claim business impact that the data cannot establish.
