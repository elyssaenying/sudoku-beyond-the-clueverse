from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_ARCHIVE = ROOT / "data" / "raw" / "sudoku_3m.zip"
OUTPUT_DIR = ROOT / "data" / "processed"
TABLEAU_DATA_DIR = ROOT / "tableau" / "Data" / "sudoku"
EXPECTED_SHA256 = "8a54b8864acacc6df483896709357e1de1a68391a079b37f5d8ec4e0bb1442f3"
RANDOM_SEED = 20260917
SAMPLE_SIZE = 100_000
DASHBOARD_CLUE_MIN = 21
DASHBOARD_CLUE_MAX = 28


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def provisional_tier(rating: pd.Series) -> pd.Series:
    return pd.cut(
        rating,
        bins=[-np.inf, 0.0, 2.0, 4.0, np.inf],
        labels=["Beginner", "Intermediate", "Advanced", "Expert"],
        include_lowest=True,
    )


def puzzle_features(puzzle: str) -> dict[str, float]:
    present = np.fromiter((character != "." for character in puzzle), dtype=np.int8, count=81).reshape(9, 9)
    row_counts = present.sum(axis=1)
    column_counts = present.sum(axis=0)
    box_counts = np.array(
        [present[row : row + 3, column : column + 3].sum() for row in (0, 3, 6) for column in (0, 3, 6)]
    )
    digit_counts = np.array([puzzle.count(str(digit)) for digit in range(1, 10)])
    return {
        "row_clue_sd": float(row_counts.std()),
        "column_clue_sd": float(column_counts.std()),
        "box_clue_sd": float(box_counts.std()),
        "digit_clue_sd": float(digit_counts.std()),
        "rotational_symmetry": float((present == np.rot90(present, 2)).mean()),
        "centre_is_clue": int(present[4, 4]),
        "minimum_row_clues": int(row_counts.min()),
        "minimum_column_clues": int(column_counts.min()),
        "minimum_box_clues": int(box_counts.min()),
        "corner_clues": int(present[0, 0] + present[0, 8] + present[8, 0] + present[8, 8]),
        "edge_clues": int(present[0, :].sum() + present[8, :].sum() + present[1:8, 0].sum() + present[1:8, 8].sum()),
    }


def fit_ordinary_least_squares(train_x: np.ndarray, train_y: np.ndarray, test_x: np.ndarray) -> np.ndarray:
    train_design = np.column_stack([np.ones(len(train_x)), train_x])
    test_design = np.column_stack([np.ones(len(test_x)), test_x])
    coefficients, *_ = np.linalg.lstsq(train_design, train_y, rcond=None)
    return test_design @ coefficients


def regression_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    residual_sum = float(np.square(actual - predicted).sum())
    total_sum = float(np.square(actual - actual.mean()).sum())
    return {
        "mae": float(np.abs(actual - predicted).mean()),
        "rmse": float(np.sqrt(np.square(actual - predicted).mean())),
        "r_squared": float(1 - residual_sum / total_sum),
    }


def main() -> None:
    if not RAW_ARCHIVE.exists():
        raise FileNotFoundError(f"Missing source archive: {RAW_ARCHIVE}")

    archive_hash = file_sha256(RAW_ARCHIVE)
    if archive_hash != EXPECTED_SHA256:
        raise ValueError(f"Unexpected source SHA-256: {archive_hash}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TABLEAU_DATA_DIR.mkdir(parents=True, exist_ok=True)
    data = pd.read_csv(RAW_ARCHIVE, compression="zip", dtype={"id": "int64", "puzzle": "string", "solution": "string"})

    missing_values = int(data.isna().sum().sum())
    duplicate_ids = int(data["id"].duplicated().sum())
    duplicate_puzzles = int(data["puzzle"].duplicated().sum())
    valid_puzzle_characters = data["puzzle"].str.fullmatch(r"[1-9.]{81}", na=False)
    valid_solution_characters = data["solution"].str.fullmatch(r"[1-9]{81}", na=False)
    actual_clues = data["puzzle"].str.count(r"[1-9]")
    clue_count_mismatches = int((actual_clues != data["clues"]).sum())

    solution_sample = data.sample(n=min(50_000, len(data)), random_state=RANDOM_SEED)

    def valid_solution_grid(solution: str) -> bool:
        expected = set("123456789")
        rows = [solution[index : index + 9] for index in range(0, 81, 9)]
        columns = [solution[index::9] for index in range(9)]
        boxes = [
            "".join(solution[(row + offset_row) * 9 + column + offset_column] for offset_row in range(3) for offset_column in range(3))
            for row in (0, 3, 6)
            for column in (0, 3, 6)
        ]
        return all(set(group) == expected for group in rows + columns + boxes)

    invalid_sampled_solutions = int((~solution_sample["solution"].map(valid_solution_grid)).sum())
    sampled_givens_match_solution = solution_sample.apply(
        lambda row: all(
            given == "." or given == solved
            for given, solved in zip(row["puzzle"], row["solution"])
        ),
        axis=1,
    )
    sampled_givens_mismatches = int((~sampled_givens_match_solution).sum())

    pearson = float(data[["clues", "difficulty"]].corr(method="pearson").iloc[0, 1])
    spearman = float(data[["clues", "difficulty"]].corr(method="spearman").iloc[0, 1])
    data["difficulty_tier"] = provisional_tier(data["difficulty"])

    validation = pd.DataFrame(
        [
            ["Source archive SHA-256 mismatch", "Full source", int(archive_hash != EXPECTED_SHA256), 0],
            ["Missing values", "Full source", missing_values, 0],
            ["Duplicate IDs", "Full source", duplicate_ids, 0],
            ["Duplicate puzzle strings", "Full source", duplicate_puzzles, 0],
            ["Invalid puzzle length or characters", "Full source", int((~valid_puzzle_characters).sum()), 0],
            ["Invalid solution length or characters", "Full source", int((~valid_solution_characters).sum()), 0],
            ["Reported clue-count mismatches", "Full source", clue_count_mismatches, 0],
            ["Invalid completed solution grids", f"Deterministic sample of {len(solution_sample):,}", invalid_sampled_solutions, 0],
            ["Puzzle givens conflict with supplied solution", f"Deterministic sample of {len(solution_sample):,}", sampled_givens_mismatches, 0],
        ],
        columns=["check", "scope", "observed_issues", "expected_issues"],
    )
    validation["status"] = np.where(validation["observed_issues"] == validation["expected_issues"], "Pass", "Review")
    validation.to_csv(OUTPUT_DIR / "validation_summary.csv", index=False)

    grouped = data.groupby("clues", observed=True)["difficulty"]
    clue_summary = grouped.agg(
        puzzle_count="size",
        mean_rating="mean",
        median_rating="median",
        rating_sd="std",
        minimum_rating="min",
        maximum_rating="max",
    )
    quantiles = grouped.quantile([0.10, 0.25, 0.75, 0.90]).unstack()
    quantiles.columns = ["rating_p10", "rating_p25", "rating_p75", "rating_p90"]
    clue_summary = clue_summary.join(quantiles)
    clue_summary["scanning_only_share"] = grouped.apply(lambda values: float((values == 0).mean()))
    clue_summary["expert_share"] = grouped.apply(lambda values: float((values > 4).mean()))
    clue_summary = clue_summary.reset_index()
    clue_summary["rating_range"] = clue_summary["maximum_rating"] - clue_summary["minimum_rating"]
    # Prefer this robust spread measure in the dashboard so a single extreme
    # puzzle cannot exaggerate how mixed a clue-count bucket usually is.
    clue_summary["central_80_range"] = clue_summary["rating_p90"] - clue_summary["rating_p10"]
    clue_summary.to_csv(OUTPUT_DIR / "clue_difficulty_summary.csv", index=False, float_format="%.6f")
    dashboard_clue_summary = clue_summary.loc[
        clue_summary["clues"].between(DASHBOARD_CLUE_MIN, DASHBOARD_CLUE_MAX)
    ]
    dashboard_clue_summary.to_csv(
        TABLEAU_DATA_DIR / "clue_difficulty_summary.csv",
        index=False,
        float_format="%.6f",
    )

    heatmap = data.groupby(["clues", "difficulty"], observed=True).size().rename("puzzle_count").reset_index()
    heatmap["share_within_clue_count"] = heatmap["puzzle_count"] / heatmap.groupby("clues")["puzzle_count"].transform("sum")
    heatmap.to_csv(OUTPUT_DIR / "difficulty_heatmap.csv", index=False, float_format="%.8f")

    tier_summary = (
        data.groupby("difficulty_tier", observed=True)["difficulty"]
        .agg(puzzle_count="size", minimum_rating="min", maximum_rating="max", average_rating="mean")
        .reset_index()
    )
    tier_summary["catalogue_share"] = tier_summary["puzzle_count"] / len(data)
    tier_summary.to_csv(OUTPUT_DIR / "tier_summary.csv", index=False, float_format="%.8f")

    sample = data.sample(n=min(SAMPLE_SIZE, len(data)), random_state=RANDOM_SEED).copy().reset_index(drop=True)
    feature_table = pd.DataFrame([puzzle_features(puzzle) for puzzle in sample["puzzle"]])
    sample = pd.concat([sample, feature_table], axis=1)
    sample["actual_clues"] = sample["puzzle"].str.count(r"[1-9]")
    sample.to_csv(OUTPUT_DIR / "structural_sample.csv", index=False, float_format="%.6f")

    feature_columns = [
        "clues",
        "row_clue_sd",
        "column_clue_sd",
        "box_clue_sd",
        "digit_clue_sd",
        "rotational_symmetry",
        "centre_is_clue",
        "minimum_row_clues",
        "minimum_column_clues",
        "minimum_box_clues",
        "corner_clues",
        "edge_clues",
    ]
    correlations = (
        sample[feature_columns + ["difficulty"]]
        .corr(method="pearson")["difficulty"]
        .drop("difficulty")
        .rename("pearson_correlation")
        .rename_axis("feature")
        .reset_index()
    )
    correlations["absolute_correlation"] = correlations["pearson_correlation"].abs()
    correlations = correlations.sort_values("absolute_correlation", ascending=False)
    correlations.to_csv(OUTPUT_DIR / "feature_correlations.csv", index=False, float_format="%.8f")

    rng = np.random.default_rng(RANDOM_SEED)
    order = rng.permutation(len(sample))
    split = int(len(sample) * 0.80)
    train_index, test_index = order[:split], order[split:]
    actual_train = sample.loc[train_index, "difficulty"].to_numpy(dtype=float)
    actual_test = sample.loc[test_index, "difficulty"].to_numpy(dtype=float)

    clue_categories = sorted(sample["clues"].unique())
    baseline_features = np.column_stack([(sample["clues"].to_numpy() == clue).astype(float) for clue in clue_categories[1:]])
    expanded_features = sample[feature_columns].to_numpy(dtype=float)
    means = expanded_features[train_index].mean(axis=0)
    standard_deviations = expanded_features[train_index].std(axis=0)
    standard_deviations[standard_deviations == 0] = 1
    expanded_features = (expanded_features - means) / standard_deviations

    baseline_prediction = fit_ordinary_least_squares(
        baseline_features[train_index], actual_train, baseline_features[test_index]
    )
    expanded_prediction = fit_ordinary_least_squares(
        expanded_features[train_index], actual_train, expanded_features[test_index]
    )
    model_rows = []
    for model_name, prediction, feature_count in (
        ("Clue count only", baseline_prediction, len(clue_categories) - 1),
        ("Visible surface features", expanded_prediction, len(feature_columns)),
    ):
        metrics = regression_metrics(actual_test, prediction)
        model_rows.append(
            {
                "model": model_name,
                "test_rows": len(actual_test),
                "feature_count": feature_count,
                **metrics,
            }
        )
    model_comparison = pd.DataFrame(model_rows)
    model_comparison.to_csv(OUTPUT_DIR / "model_comparison.csv", index=False, float_format="%.8f")

    low_clue_easy = data[(data["clues"] <= 22) & (data["difficulty"] == 0)].nsmallest(50, ["clues", "id"]).copy()
    low_clue_easy["anomaly_type"] = "Few clues, scanning-only rating"
    high_clue_hard = data[(data["clues"] >= 27) & (data["difficulty"] > 4)].nlargest(50, ["difficulty", "clues"]).copy()
    high_clue_hard["anomaly_type"] = "Many clues, expert rating"
    same_clues_extremes = pd.concat(
        [
            data[data["clues"] == 23].nsmallest(25, ["difficulty", "id"]),
            data[data["clues"] == 23].nlargest(25, ["difficulty", "id"]),
        ],
        ignore_index=True,
    )
    same_clues_extremes["anomaly_type"] = "Same clue count, opposite difficulty"
    anomalies = pd.concat([low_clue_easy, high_clue_hard, same_clues_extremes], ignore_index=True)
    anomalies.to_csv(OUTPUT_DIR / "anomaly_examples.csv", index=False)

    beginner_share = float((data["difficulty"] == 0).mean())
    expert_share = float((data["difficulty"] > 4).mean())
    clue_23 = clue_summary.loc[clue_summary["clues"] == 23].iloc[0]
    model_surface_r2 = float(model_comparison.loc[model_comparison["model"] == "Visible surface features", "r_squared"].iloc[0])
    kpis = pd.DataFrame(
        [
            ["Records analysed", float(len(data)), "count", "Full source"],
            ["Pearson correlation: clues vs rating", pearson, "correlation", "Full source"],
            ["Spearman correlation: clues vs rating", spearman, "correlation", "Full source"],
            ["Scanning-only share", beginner_share, "percentage", "Full source"],
            ["Expert share", expert_share, "percentage", "Full source"],
            ["23-clue minimum rating", float(clue_23["minimum_rating"]), "rating", "Full source"],
            ["23-clue maximum rating", float(clue_23["maximum_rating"]), "rating", "Full source"],
            ["Surface-feature model test R-squared", model_surface_r2, "r_squared", f"Deterministic sample of {len(sample):,}"],
        ],
        columns=["metric", "value", "format", "scope"],
    )
    kpis.to_csv(OUTPUT_DIR / "dashboard_kpis.csv", index=False, float_format="%.10f")

    run_summary = {
        "source_rows": int(len(data)),
        "source_sha256": archive_hash,
        "pearson_clues_difficulty": pearson,
        "spearman_clues_difficulty": spearman,
        "beginner_share": beginner_share,
        "expert_share": expert_share,
        "surface_feature_test_r_squared": model_surface_r2,
        "output_files": sorted(path.name for path in OUTPUT_DIR.glob("*.csv")),
    }
    (OUTPUT_DIR / "run_summary.json").write_text(json.dumps(run_summary, indent=2), encoding="utf-8")
    print(json.dumps(run_summary, indent=2))


if __name__ == "__main__":
    main()
