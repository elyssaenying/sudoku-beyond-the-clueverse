# Portfolio storyline

## Personal starting point

I had played Sudoku casually for months, and many patterns had become almost automatic. When I watched friends struggle with puzzles that felt straightforward to me, I began questioning what a difficulty label actually represents. Does a puzzle become harder simply because it has fewer clues, or because of the reasoning needed to progress?

## From observation to product problem

Difficulty labels help players choose an appropriate puzzle, but a digital Sudoku product may need to classify thousands or millions of generated boards. An inconsistent labelling method can place visually similar puzzles into very different solving experiences.

The product question is:

> Can a Sudoku app use simple puzzle characteristics to assign dependable difficulty tiers, or should it rely on solver-based complexity measures?

The dashboard audience is a product manager or puzzle-content lead. The end users are Sudoku players selecting a challenge. The project does not invent demographic segments; the available data describes puzzles, not people.

## Research basis

Research by Radek Pelánek found that Sudoku difficulty is influenced by the complexity of individual logic steps and the dependency structure between those steps. Computational models of human solving performed better than simplistic metrics.

Source: [Difficulty Rating of Sudoku Puzzles: An Overview and Evaluation](https://arxiv.org/abs/1403.7373)

## Analysis narrative

1. Validate three million puzzle records and document the source limitations.
2. Test whether clue count is associated with the supplied solver rating.
3. Engineer visible structural features such as row, column and box imbalance and rotational symmetry.
4. Compare a clue-only model with a broader surface-feature model on unseen data.
5. Examine puzzles that violate the intuitive fewer-clues-equals-harder rule.
6. Translate the evidence into a difficulty-labelling recommendation and a next-step measurement plan.

## Responsible conclusion

The supplied rating is produced by an automated solver, not by human players. The analysis can evaluate catalogue classification, but it cannot establish effects on enjoyment, engagement or retention. A production team should validate final tiers using completion time, hint usage, error counts and abandonment by player skill level.

