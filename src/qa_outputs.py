from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
TABLEAU_DATA = ROOT / "tableau" / "Data" / "sudoku" / "clue_difficulty_summary.csv"
EXPECTED_ROWS = 3_000_000
EXPECTED_SAMPLE_ROWS = 100_000
EXPECTED_DASHBOARD_ROWS = 2_999_482


def main() -> None:
    validation = pd.read_csv(DATA / "validation_summary.csv")
    clue_summary = pd.read_csv(DATA / "clue_difficulty_summary.csv")
    heatmap = pd.read_csv(DATA / "difficulty_heatmap.csv")
    tiers = pd.read_csv(DATA / "tier_summary.csv")
    sample = pd.read_csv(DATA / "structural_sample.csv")
    models = pd.read_csv(DATA / "model_comparison.csv")
    kpis = pd.read_csv(DATA / "dashboard_kpis.csv")
    tableau_data = pd.read_csv(TABLEAU_DATA)

    assert validation["status"].eq("Pass").all(), "At least one source validation check requires review."
    assert int(clue_summary["puzzle_count"].sum()) == EXPECTED_ROWS
    assert int(heatmap["puzzle_count"].sum()) == EXPECTED_ROWS
    assert int(tiers["puzzle_count"].sum()) == EXPECTED_ROWS
    assert abs(float(tiers["catalogue_share"].sum()) - 1.0) < 1e-7
    assert len(sample) == EXPECTED_SAMPLE_ROWS
    assert sample["id"].is_unique
    assert sample["clues"].eq(sample["actual_clues"]).all()
    assert not sample.isna().any().any()
    assert set(models["model"]) == {"Clue count only", "Visible surface features"}

    values = dict(zip(kpis["metric"], kpis["value"]))
    assert int(values["Records analysed"]) == EXPECTED_ROWS
    assert abs(values["Pearson correlation: clues vs rating"]) < 0.10
    assert abs(values["Spearman correlation: clues vs rating"]) < 0.10
    assert values["Surface-feature model test R-squared"] < 0.10
    assert values["23-clue minimum rating"] == 0.0
    assert values["23-clue maximum rating"] == 8.5
    assert set(tableau_data["clues"]) == set(range(21, 29))
    assert int(tableau_data["puzzle_count"].sum()) == EXPECTED_DASHBOARD_ROWS

    print("QA passed: source totals reconcile, the Tableau view is scoped correctly, and hypothesis metrics match the exported tables.")


if __name__ == "__main__":
    main()
