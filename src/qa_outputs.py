from html.parser import HTMLParser
from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
TABLEAU_DATA = ROOT / "tableau" / "Data" / "sudoku" / "clue_difficulty_summary.csv"
EXPECTED_ROWS = 3_000_000
EXPECTED_SAMPLE_ROWS = 100_000
EXPECTED_DASHBOARD_ROWS = 2_999_482
HERO_PUZZLE_ID = 2_760_549


class WebsitePuzzleParser(HTMLParser):
    """Read the displayed starting clues, answer and caption from the website."""

    def __init__(self) -> None:
        super().__init__()
        self.in_grid = False
        self.in_cell = False
        self.in_note = False
        self.cell_text = ""
        self.cells: list[str] = []
        self.solution = ""
        self.notes: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        classes = (attributes.get("class") or "").split()
        if tag == "div" and "sudoku-grid" in classes:
            self.in_grid = True
            self.solution = attributes.get("data-solution") or ""
        elif self.in_grid and tag == "span":
            self.in_cell = True
            self.cell_text = ""
        elif tag == "p" and "visual-note" in classes:
            self.in_note = True

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.cell_text += data
        if self.in_note:
            self.notes.append(data)

    def handle_endtag(self, tag: str) -> None:
        if self.in_grid and tag == "span":
            self.cells.append(self.cell_text.strip() or ".")
            self.in_cell = False
        elif self.in_grid and tag == "div":
            self.in_grid = False
        elif self.in_note and tag == "p":
            self.in_note = False


def count_solutions(puzzle: str, limit: int = 2) -> int:
    board = [0 if value == "." else int(value) for value in puzzle]
    rows = [set(range(1, 10)) for _ in range(9)]
    columns = [set(range(1, 10)) for _ in range(9)]
    boxes = [set(range(1, 10)) for _ in range(9)]

    for index, value in enumerate(board):
        if value == 0:
            continue
        row, column = divmod(index, 9)
        box = (row // 3) * 3 + column // 3
        if value not in rows[row] or value not in columns[column] or value not in boxes[box]:
            return 0
        rows[row].remove(value)
        columns[column].remove(value)
        boxes[box].remove(value)

    solutions = 0

    def search() -> None:
        nonlocal solutions
        if solutions >= limit:
            return
        candidates = []
        for index, value in enumerate(board):
            if value != 0:
                continue
            row, column = divmod(index, 9)
            box = (row // 3) * 3 + column // 3
            options = rows[row] & columns[column] & boxes[box]
            if not options:
                return
            candidates.append((len(options), index, options))
        if not candidates:
            solutions += 1
            return
        _, index, options = min(candidates, key=lambda item: item[0])
        row, column = divmod(index, 9)
        box = (row // 3) * 3 + column // 3
        for option in options:
            board[index] = option
            rows[row].remove(option)
            columns[column].remove(option)
            boxes[box].remove(option)
            search()
            boxes[box].add(option)
            columns[column].add(option)
            rows[row].add(option)
            board[index] = 0

    search()
    return solutions


def main() -> None:
    validation = pd.read_csv(DATA / "validation_summary.csv")
    clue_summary = pd.read_csv(DATA / "clue_difficulty_summary.csv")
    heatmap = pd.read_csv(DATA / "difficulty_heatmap.csv")
    tiers = pd.read_csv(DATA / "tier_summary.csv")
    sample = pd.read_csv(DATA / "structural_sample.csv")
    models = pd.read_csv(DATA / "model_comparison.csv")
    kpis = pd.read_csv(DATA / "dashboard_kpis.csv")
    hero_records = pd.read_csv(DATA / "hero_puzzle.csv")
    tableau_data = pd.read_csv(TABLEAU_DATA)

    assert validation["status"].eq("Pass").all(), "At least one source validation check requires review."
    assert int(clue_summary["puzzle_count"].sum()) == EXPECTED_ROWS
    assert int(heatmap["puzzle_count"].sum()) == EXPECTED_ROWS
    assert int(tiers["puzzle_count"].sum()) == EXPECTED_ROWS
    assert abs(float(tiers["catalogue_share"].sum()) - 1.0) < 1e-7
    assert abs(float((clue_summary["rating_p90"] - clue_summary["rating_p10"] - clue_summary["central_80_range"]).fillna(0).abs().max())) < 1e-7
    assert len(sample) == EXPECTED_SAMPLE_ROWS
    assert sample["id"].is_unique
    assert sample["clues"].eq(sample["actual_clues"]).all()
    assert not sample.isna().any().any()
    assert set(models["model"]) == {"Clue count only", "Visible surface features"}
    assert set(models["test_rows"]) == {20_000}
    assert dict(zip(models["model"], models["feature_count"])) == {
        "Clue count only": 10,
        "Visible surface features": 12,
    }

    values = dict(zip(kpis["metric"], kpis["value"]))
    assert int(values["Records analysed"]) == EXPECTED_ROWS
    assert abs(values["Pearson correlation: clues vs rating"]) < 0.10
    assert abs(values["Spearman correlation: clues vs rating"]) < 0.10
    assert values["Surface-feature model test R-squared"] < 0.10
    assert values["23-clue minimum rating"] == 0.0
    assert values["23-clue maximum rating"] == 8.5
    assert abs(values["Scanning-only share"] - float(tiers.loc[tiers["minimum_rating"] == 0, "catalogue_share"].iloc[0])) < 1e-7
    assert abs(values["Expert share"] - float(tiers.loc[tiers["minimum_rating"] > 4, "catalogue_share"].iloc[0])) < 1e-7
    assert abs(
        values["Surface-feature model test R-squared"]
        - float(models.loc[models["model"] == "Visible surface features", "r_squared"].iloc[0])
    ) < 1e-7
    assert set(tableau_data["clues"]) == set(range(21, 29))
    assert int(tableau_data["puzzle_count"].sum()) == EXPECTED_DASHBOARD_ROWS
    assert_frame_equal(
        tableau_data.reset_index(drop=True),
        clue_summary.loc[clue_summary["clues"].between(21, 28)].reset_index(drop=True),
        check_dtype=False,
        atol=1e-7,
    )

    hero = hero_records.loc[hero_records["id"] == HERO_PUZZLE_ID]
    assert len(hero) == 1
    hero = hero.iloc[0]
    assert int(hero["clues"]) == 23 and float(hero["difficulty"]) == 6.8
    website = WebsitePuzzleParser()
    website.feed((ROOT / "index.html").read_text(encoding="utf-8"))
    assert len(website.cells) == 81, "The website grid must contain 81 cells."
    assert "".join(website.cells) == hero["puzzle"], "The website starting clues do not match the source puzzle."
    assert website.solution == hero["solution"], "The playable website answer does not match the source solution."
    caption = " ".join(website.notes)
    assert f"ID {HERO_PUZZLE_ID}" in caption and "23 clues" in caption and "computer rating 6.8" in caption
    assert len(hero["solution"]) == 81 and count_solutions(hero["solution"]) == 1
    assert all(given == "." or given == solved for given, solved in zip(hero["puzzle"], hero["solution"]))
    assert count_solutions(hero["puzzle"]) == 1

    print(
        "QA passed: source totals reconcile, Tableau data matches the processed source, "
        "hypothesis metrics agree across outputs, and the website puzzle and answer match "
        "source record 2760549 with exactly one solution."
    )


if __name__ == "__main__":
    main()
