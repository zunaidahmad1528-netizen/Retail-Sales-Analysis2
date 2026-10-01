import sys
from pathlib import Path

import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))
from analysis import clean_data, compute_kpis, revenue_by


def sample_df():
    return pd.DataFrame({
        "order_date": ["2026-01-05", "2026-01-05", "2026-02-10", "bad-date"],
        "category": ["A", "A", "B", "A"],
        "region": ["N", "N", "S", "N"],
        "quantity": [2, 2, 3, 1],
        "unit_price": [10, 10, 5, 10],
    })


def test_clean_data_removes_duplicates_and_bad_rows():
    df = clean_data(sample_df())
    assert len(df) == 2
    assert "revenue" in df.columns


def test_compute_kpis():
    kpis = compute_kpis(clean_data(sample_df()))
    assert kpis["total_revenue"] == 35
    assert kpis["total_orders"] == 2
    assert kpis["top_category"] == "A"


def test_revenue_by_is_sorted_highest_first():
    result = revenue_by(clean_data(sample_df()), "category")
    assert result.iloc[0]["category"] == "A"
