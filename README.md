# Sudoku: Beyond the Clue-Verse

What three million rated puzzles reveal about Sudoku difficulty labels. This project asks whether counting the starting numbers, or summarising where they sit, helps predict a puzzle's computer difficulty rating. Clue count showed almost no link, and the two tested prediction rules performed poorly.

**Live website:** [sudoku-beyond-the-clueverse.vercel.app](https://sudoku-beyond-the-clueverse.vercel.app/)

## Website

The repository root contains a responsive website (`index.html`, `styles.css`, and `script.js`). It presents the question and answer first, then the Tableau dashboard, personal motivation, findings, recommendation, methods and limits. The top Sudoku is playable, highlights incorrect entries and turns green when solved. Restart clears the player's entries. An optional Earth-42 visual mode is activated by pressing or tapping `4`, then `2`. The site is deployed on Vercel and uses no paid UI libraries or subscriptions.

The pre–Clue-Verse website is preserved on the `original-design` branch. After both branches are pushed, it can be viewed from GitHub’s branch selector or restored locally with `git switch original-design`; return to the approved version with `git switch main`.

## Business question

Can a Sudoku app use clue count and basic layout measurements to help label puzzle difficulty, and what other evidence should it collect?

The dashboard is designed for a product manager or puzzle-content lead responsible for difficulty labels and catalogue quality. It does not claim that difficulty causes retention or revenue because the source contains no player-behaviour data.

## Hypotheses

- **H1, clue-count usefulness:** clue count has at least a weak practical relationship with the supplied rating (`|r| ≥ 0.10`).
- **H2, tested layout-model usefulness:** a linear model combining clue count and basic layout measurements explains at least 10% of rating differences on puzzles kept out of training (`R² ≥ 0.10`).

Neither met the project's cutoff. These cutoffs are project decision rules, not universal standards. They were set before the final dashboard was built. The results apply to this dataset, the chosen measurements and the tested models. They do not rule out every clue arrangement, solving technique or more complex model. The source ratings describe computer solving, not difficulty measured from real players.

## Repository structure

```text
data/
  raw/          Source archive and provenance notes; large files are ignored by Git
  processed/    Tableau-ready analytical tables
docs/           Storyline, methodology and Tableau build specification
src/            Reproducible data preparation and analysis
tableau/        Tableau workbook plus its small, local display dataset
```

## Reproduce the analysis

1. Place `sudoku_3m.zip` in `data/raw/`. The archive must contain `sudoku-3m.csv`.
2. Create a Python environment and install `requirements.txt`.
3. Run:

```bash
python src/prepare_analysis.py
python src/qa_outputs.py
```

The script validates full-source structure and identifiers, checks solution-grid and given-to-solution consistency on a deterministic 50,000-row sample, computes full-population summaries, engineers surface features on a deterministic 100,000-row sample and exports the tables used by Tableau. The diagnostic models use one reproducible 80/20 split, leaving 20,000 rows unseen during fitting.

It also exports `data/processed/hero_puzzle.csv` directly from source record 2760549. The QA script checks the website's 81 cells, answer and caption against this record and verifies that the puzzle has exactly one solution.

Open `tableau/Sudoku Difficulty Audit.twb` in Tableau Desktop. Its three charts intentionally show clue counts 21–28, which contain 2,999,482 of the 3,000,000 records (99.98%). The full-population KPIs, correlations and grouped summaries use every source row; the surface-feature model uses the documented 100,000-row sample.

## Data source

David Radcliffe, [3 million Sudoku puzzles with ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings), CC0 Public Domain. The supplied rating is based on average automated-solver search-tree depth over ten attempts; it is not observed human solving time.

## Decision

Avoid using clue count as the main difficulty label. The tested rules using clue count and basic layout measurements also predicted computer ratings poorly. Start new puzzles with a computer estimate, then collect real player results to improve the labels. Compare time taken, hints, mistakes, restarts and giving up separately by player skill. If one label is needed for everyone, combine the groups' results in proportions that reflect the app's players.

This player-based approach is a recommendation for future work. No player results were collected or analysed in this project.

## Illustration source

The hanging Spider-Man image was supplied as a reference during development. The original artist and source link have not yet been identified. See [illustration credits](docs/illustration_credits.md) for the recorded information; the dataset's CC0 status does not describe this illustration.
