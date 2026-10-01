"""Retail sales analysis pipeline: load, clean, analyze and visualize."""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Render charts to files without needing a display
import matplotlib.pyplot as plt
import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {"order_date", "category", "region", "quantity", "unit_price"}


def load_data(path: Path) -> pd.DataFrame:
    """Load the CSV file and standardize column names."""
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    logger.info("Loaded %d rows from %s", len(df), path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Remove duplicates and invalid rows, then add derived columns."""
    before = len(df)
    df = df.drop_duplicates().copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df = df.dropna(subset=["order_date", "quantity", "unit_price"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["order_date"].dt.to_period("M").astype(str)
    logger.info("Cleaning removed %d rows, %d remain", before - len(df), len(df))
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    """Return headline metrics. Assumes each row is one order."""
    return {
        "total_revenue": round(df["revenue"].sum(), 2),
        "total_orders": len(df),
        "avg_order_value": round(df["revenue"].mean(), 2),
        "top_category": df.groupby("category")["revenue"].sum().idxmax(),
    }


def revenue_by(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Total revenue grouped by a column, highest first."""
    return (
        df.groupby(column, as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
    )


def plot_bar(data: pd.DataFrame, x: str, title: str, out_path: Path) -> None:
    """Save a bar chart of revenue for the given column."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(data[x], data["revenue"], color="#1f4e79")
    ax.set_title(title, fontweight="bold")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info("Saved chart: %s", out_path)


def plot_monthly_trend(df: pd.DataFrame, out_path: Path) -> None:
    """Save a line chart of revenue by month."""
    monthly = df.groupby("month")["revenue"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(monthly.index, monthly.values, marker="o", color="#1f4e79")
    ax.set_title("Monthly Revenue Trend", fontweight="bold")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)
    logger.info("Saved chart: %s", out_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Retail sales analysis pipeline")
    parser.add_argument("--input", type=Path, default=Path("data/sample_sales.csv"))
    parser.add_argument("--output", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    args.output.mkdir(parents=True, exist_ok=True)
    df = clean_data(load_data(args.input))

    for name, value in compute_kpis(df).items():
        logger.info("%s: %s", name, value)

    plot_bar(revenue_by(df, "category"), "category",
             "Revenue by Category", args.output / "revenue_by_category.png")
    plot_bar(revenue_by(df, "region"), "region",
             "Revenue by Region", args.output / "revenue_by_region.png")
    plot_monthly_trend(df, args.output / "monthly_trend.png")


if __name__ == "__main__":
    main()
