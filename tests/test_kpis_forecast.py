import pandas as pd

from salesanalytics.kpis import month_over_month_growth, revenue_contribution
from salesanalytics.ml.forecast import moving_average_forecast


def sample_df():
    return pd.DataFrame({
        "order_date": ["2026-01-01", "2026-01-15", "2026-02-01", "2026-03-01"],
        "sales": [100, 200, 300, 600],
        "region": ["A", "A", "B", "B"],
        "product": ["X", "Y", "X", "Z"],
    })


def test_month_over_month_growth():
    result = month_over_month_growth(sample_df())
    assert "growth_pct" in result.columns
    assert len(result) == 3


def test_revenue_contribution():
    result = revenue_contribution(sample_df(), "region")
    assert round(result["contribution_pct"].sum(), 1) == 100.0


def test_moving_average_forecast():
    result = moving_average_forecast(sample_df(), periods=2)
    assert len(result) == 2
    assert "forecast_sales" in result.columns
