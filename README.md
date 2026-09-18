# Sudoku: Beyond the Clue-Verse

What three million rated puzzles reveal—and do not reveal—about Sudoku difficulty labels. This portfolio data-analysis project tests whether a Sudoku product can use clue count and visible grid structure to assign dependable difficulty labels.

**Live portfolio:** [sudoku-beyond-the-clueverse.vercel.app](https://sudoku-beyond-the-clueverse.vercel.app/)

## Portfolio site

The repository root contains a dependency-free, responsive case-study website (`index.html`, `styles.css`, and `script.js`). It presents the business question and answer first, then the Tableau dashboard, personal motivation, evidence, recommendation, methodology and limitations. An optional Earth-42 visual mode is hidden behind the `4`, `2` interaction without changing the analytical content. The site is ready for a free static deployment such as Vercel Hobby; no paid UI libraries or subscriptions are required.

The pre–Clue-Verse website is preserved on the `original-design` branch. After both branches are pushed, it can be viewed from GitHub’s branch selector or restored locally with `git switch original-design`; return to the approved version with `git switch main`.

## Business question

Can a Sudoku app use clue count and basic visible structure to assign dependable provisional difficulty tiers, and what evidence should determine the final player-facing labels?

The dashboard is designed for a product manager or puzzle-content lead responsible for difficulty labels and catalogue quality. It does not claim that difficulty causes retention or revenue because the source contains no player-behaviour data.

## Hypotheses

- **H1 — clue-count usefulness:** clue count has at least a weak practical relationship with the supplied rating (`|r| ≥ 0.10`).
- **H2 — surface-feature usefulness:** visible grid features explain enough out-of-sample rating variation to support classification (`R² ≥ 0.10`).

Neither hypothesis is supported. The `0.10` cutoffs are project decision rules, not universal statistical standards. They were set before the final dashboard was built and are intentionally lenient: results far below them are not useful for the product decision. Exploratory questions about catalogue balance, provisional rating bands and misleading puzzle layouts are kept separate.

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

Open `tableau/Sudoku Difficulty Audit.twb` in Tableau Desktop. Its three charts intentionally show clue counts 21–28, which contain 2,999,482 of the 3,000,000 records (99.98%). The full-population KPIs, correlations and grouped summaries use every source row; the surface-feature model uses the documented 100,000-row sample.

## Data source

David Radcliffe, [3 million Sudoku puzzles with ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings), CC0 Public Domain. The supplied rating is based on average automated-solver search-tree depth over ten attempts; it is not observed human solving time.

## Decision

Clue count and the tested surface summaries are not dependable primary labels. Use solver complexity only to provisionally tier new puzzles. Once enough gameplay exists, let completion time, hints, mistakes, restarts and abandonment determine player-facing labels within demonstrated skill groups. If the product requires one catalogue-wide label, combine group-level results using transparent weights that reflect its player base.
