# Portfolio storyline

## Personal starting point

After years of playing Sudoku, I had picked up enough techniques and tricks to know that fewer clues did not always mean a harder puzzle. I suspected that where the clues were placed mattered more than how many there were. But when friends found puzzles I considered relatively easy just as difficult as the others, I began questioning what difficulty meant and whether it came from the puzzle, the player or both.

## From observation to product problem

Difficulty labels help players choose an appropriate puzzle, but a digital Sudoku product may need to classify thousands or millions of generated boards. An inconsistent labelling method can give players unreliable expectations.

The product question is:

> Can a Sudoku app use clue count and basic visible structure to assign dependable provisional difficulty tiers, and what evidence should determine the final player-facing labels?

The dashboard audience is a product manager or puzzle-content lead. The end users are Sudoku players selecting a challenge. The project does not invent demographic segments; the available data describes puzzles, not people.

## Research basis

Research by Radek Pelánek found that Sudoku difficulty is influenced by the complexity of individual logic steps and the dependency structure between those steps. Computational models of human solving performed better than simplistic metrics.

Source: [Difficulty Rating of Sudoku Puzzles: An Overview and Evaluation](https://arxiv.org/abs/1403.7373)

## Analysis narrative

1. Validate full-source structure, check a deterministic solution sample and document the limits of that validation.
2. Test whether clue count is associated with the supplied solver rating.
3. Engineer visible structural features such as row, column and box imbalance and rotational symmetry.
4. Compare a clue-only model with a broader surface-feature model on unseen data.
5. Examine puzzles that violate the intuitive fewer-clues-equals-harder rule.
6. Translate the evidence into a difficulty-labelling recommendation and a next-step measurement plan.

## Responsible conclusion

The supplied rating is produced by an automated solver, not by human players. The analysis can evaluate whether simple puzzle metadata is useful for provisional catalogue classification, but it cannot establish human-perceived difficulty or effects on enjoyment, engagement or retention. Use solver complexity only as a cold-start estimate. Once enough gameplay exists, calibrate labels with completion time, hints, mistakes, restarts and abandonment within demonstrated skill groups. Prefer skill-calibrated labels; if one catalogue-wide label is required, combine group-level results using transparent weights that reflect the player base.
