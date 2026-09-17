# Auditing Sudoku Difficulty at Scale

A portfolio data-analysis project testing whether a Sudoku product can use clue count and visible grid structure to assign dependable difficulty labels.

## Portfolio site

The repository root contains a dependency-free, responsive case-study website (`index.html`, `styles.css`, and `script.js`). It presents the business question and answer first, then the Tableau dashboard, personal motivation, evidence, recommendation, methodology and limitations. It is ready for a free static deployment such as Vercel Hobby; no paid UI libraries or subscriptions are required.

## Business question

Can a Sudoku app use simple puzzle characteristics to assign consistent difficulty tiers, or should it rely on solver-based complexity measures?

The dashboard is designed for a product manager or puzzle-content lead responsible for difficulty labels and catalogue quality. It does not claim that difficulty causes retention or revenue because the source contains no player-behaviour data.

## Hypotheses

- **H1 — clue-count hypothesis:** clue count has a weak relationship with the supplied difficulty rating (`|r| < 0.10`).
- **H2 — surface-feature hypothesis:** clue count, clue distribution and symmetry together have limited out-of-sample predictive power (`R² < 0.10`).

These are tested separately from the exploratory questions about catalogue balance, tier boundaries and misleading puzzle layouts.

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

The script validates the source, computes full-population summaries, engineers surface features on a deterministic sample and exports the tables used by Tableau.

Open `tableau/Sudoku Difficulty Audit.twb` in Tableau Desktop. Its three charts intentionally show clue counts 21–28, which contain 2,999,482 of the 3,000,000 records (99.98%). The full-population KPIs and statistical tests still use every source row.

## Data source

David Radcliffe, [3 million Sudoku puzzles with ratings](https://www.kaggle.com/datasets/radcliffe/3-million-sudoku-puzzles-with-ratings), CC0 Public Domain. The supplied rating is based on average automated-solver search-tree depth over ten attempts; it is not observed human solving time.
