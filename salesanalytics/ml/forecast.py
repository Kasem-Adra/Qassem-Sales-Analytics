from __future__ import annotations

import pandas as pd

from salesanalytics.core import sales_by_month


def moving_average_forecast(df: pd.DataFrame, periods: int = 3, window: int = 3) -> pd.DataFrame:
    """Generate a simple moving-average forecast from monthly sales."""
    monthly = sales_by_month(df)
    monthly["date"] = pd.to_datetime(monthly["month"] + "-01")
    monthly = monthly.sort_values("date")

    if monthly.empty:
        raise ValueError("No monthly data available for forecasting.")

    history = monthly["sales"].tolist()
    last_date = monthly["date"].max()
    forecasts = []

    for step in range(1, periods + 1):
        value = sum(history[-window:]) / min(len(history), window)
        history.append(value)
        forecast_date = last_date + pd.DateOffset(months=step)
        forecasts.append(
            {
                "month": forecast_date.to_period("M").strftime("%Y-%m"),
                "forecast_sales": round(float(value), 2),
            }
        )

    return pd.DataFrame(forecasts)
