import pandas as pd
import pytest

from salesanalytics.core import normalize_columns, sales_by_month, summarize_sales


def test_normalize_columns():
    df = pd.DataFrame({"Order Date": [], "Sales-Amount": []})
    assert list(normalize_columns(df).columns) == ["order_date", "sales_amount"]


def test_summarize_sales():
    df = pd.DataFrame({
        "order_date": ["2026-01-01", "2026-01-02"],
        "sales": [100, 200],
    })
    summary = summarize_sales(df)
    assert summary.rows == 2
    assert summary.total_sales == 300


def test_missing_required_columns():
    df = pd.DataFrame({"sales": [100]})
    with pytest.raises(ValueError):
        summarize_sales(df)


def test_sales_by_month():
    df = pd.DataFrame({
        "order_date": ["2026-01-01", "2026-01-15", "2026-02-01"],
        "sales": [100, 200, 50],
    })
    result = sales_by_month(df)
    assert list(result["sales"]) == [300, 50]
