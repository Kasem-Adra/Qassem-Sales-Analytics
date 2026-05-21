from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd


REQUIRED_COLUMNS = {"order_date", "sales"}


@dataclass(frozen=True)
class SalesSummary:
    rows: int
    total_sales: float
    average_sales: float
    min_sales: float
    max_sales: float
    unique_products: int | None = None
    unique_regions: int | None = None


def load_sales_data(path: str | Path) -> pd.DataFrame:
    """Load sales data from CSV, Excel, or JSON."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    suffix = file_path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(file_path)
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(file_path)
    if suffix == ".json":
        return pd.read_json(file_path)

    raise ValueError("Supported formats: .csv, .xlsx, .xls, .json")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names for predictable analytics."""
    result = df.copy()
    result.columns = [
        str(col).strip().lower().replace(" ", "_").replace("-", "_")
        for col in result.columns
    ]
    return result


def validate_sales_data(df: pd.DataFrame) -> None:
    """Validate required columns for sales analysis."""
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize, validate, and clean sales data."""
    data = normalize_columns(df)
    validate_sales_data(data)

    data["order_date"] = pd.to_datetime(data["order_date"], errors="coerce")
    data["sales"] = pd.to_numeric(data["sales"], errors="coerce")
    data = data.dropna(subset=["order_date", "sales"])
    data = data[data["sales"] >= 0]
    return data


def summarize_sales(df: pd.DataFrame) -> SalesSummary:
    """Return an executive numeric summary."""
    data = clean_sales_data(df)
    sales = data["sales"]

    return SalesSummary(
        rows=int(len(data)),
        total_sales=float(sales.sum()),
        average_sales=float(sales.mean()),
        min_sales=float(sales.min()),
        max_sales=float(sales.max()),
        unique_products=int(data["product"].nunique()) if "product" in data else None,
        unique_regions=int(data["region"].nunique()) if "region" in data else None,
    )


def sales_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sales by month."""
    data = clean_sales_data(df)
    data["month"] = data["order_date"].dt.to_period("M").astype(str)
    return data.groupby("month", as_index=False)["sales"].sum()


def sales_by_dimension(df: pd.DataFrame, dimension: str) -> pd.DataFrame:
    """Aggregate sales by any available dimension, such as product or region."""
    data = clean_sales_data(df)
    dimension = dimension.strip().lower().replace(" ", "_").replace("-", "_")

    if dimension not in data.columns:
        raise ValueError(f"Column not found: {dimension}")

    return (
        data.groupby(dimension, as_index=False)["sales"]
        .sum()
        .sort_values("sales", ascending=False)
    )


def top_items(df: pd.DataFrame, dimension: str, limit: int = 10) -> pd.DataFrame:
    """Return top sales contributors for a dimension."""
    return sales_by_dimension(df, dimension).head(limit)
