# Findings

## Hypothesis results

### H1: clue count is weakly related to difficulty — supported

- Pearson correlation: `0.0353`
- Spearman correlation: `0.0409`
- Pre-stated weak-association threshold: absolute correlation below `0.10`

Clue count does not provide a useful ordering of puzzle difficulty. The direction is also slightly positive in this generated catalogue, contradicting the common assumption that fewer clues automatically means a harder puzzle.

### H2: visible surface features have limited predictive power — supported

Performance on a deterministic 20,000-row test set:

| Model | MAE | RMSE | R² |
| --- | ---: | ---: | ---: |
| Clue count only | 1.0882 | 1.2705 | 0.0012 |
| Visible surface features | 1.0840 | 1.2668 | 0.0069 |

Adding clue distribution, symmetry, position and digit-balance features improves the fit only marginally. The model remains far below the pre-stated `R² < 0.10` insufficiency threshold.

## Exploratory findings

- `43.1%` of the catalogue has a rating of `0.0`, meaning the source solver can complete those puzzles using its scanning method.
- Only `2.2%` of puzzles fall into the provisional Expert tier above `4.0`.
- Puzzles with 23 clues span the entire observed rating range, from `0.0` to `8.5`.
- Puzzles with 24 clues also span almost the full range, from `0.0` to `8.2`.
- No individual visible feature in the 100,000-puzzle sample has an absolute Pearson correlation above `0.05` with difficulty.

## Product recommendation

Do not use clue count or surface appearance as the primary difficulty-labelling rule. Use a solver-based complexity measure to screen and provisionally tier puzzles. Before exposing those tiers to players, calibrate them using human completion time, hint usage, errors and abandonment, segmented by demonstrated player skill.

## Evidence boundary

The source rating reflects automated solver search-tree depth. It is not a direct measurement of human-perceived difficulty, enjoyment, engagement or retention. The project supports a catalogue-classification decision and a measurement plan; it does not claim business impact that the data cannot establish.

