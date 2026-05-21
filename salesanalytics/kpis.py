from __future__ import annotations

import pandas as pd

from .core import clean_sales_data


def month_over_month_growth(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate monthly sales and month-over-month growth percentage."""
    data = clean_sales_data(df)
    data["month"] = data["order_date"].dt.to_period("M").astype(str)
    monthly = data.groupby("month", as_index=False)["sales"].sum()
    monthly["previous_sales"] = monthly["sales"].shift(1)
    monthly["growth_pct"] = (
        (monthly["sales"] - monthly["previous_sales"]) / monthly["previous_sales"] * 100
    ).round(2)
    return monthly


def revenue_contribution(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Calculate revenue contribution percentage by dimension."""
    data = clean_sales_data(df)
    dimension = dimension.strip().lower().replace(" ", "_").replace("-", "_")

    if dimension not in data.columns:
        raise ValueError(f"Column not found: {dimension}")

    grouped = data.groupby(dimension, as_index=False)["sales"].sum()
    total = grouped["sales"].sum()
    grouped["contribution_pct"] = (grouped["sales"] / total * 100).round(2)
    return grouped.sort_values("sales", ascending=False)
