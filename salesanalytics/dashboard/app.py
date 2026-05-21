from __future__ import annotations

import pandas as pd
import streamlit as st

from salesanalytics.core import (
    sales_by_dimension,
    sales_by_month,
    summarize_sales,
)
from salesanalytics.kpis import month_over_month_growth
from salesanalytics.ml.forecast import moving_average_forecast


st.set_page_config(
    page_title="Qassem Sales Analytics",
    layout="wide",
)

st.title("Qassem Sales Analytics")
st.caption("Professional sales analytics dashboard by Kasem Adra")

uploaded = st.file_uploader(
    "Upload sales data",
    type=["csv", "xlsx", "xls", "json"],
)

if uploaded:
    suffix = uploaded.name.split(".")[-1].lower()

    if suffix == "csv":
        df = pd.read_csv(uploaded)

    elif suffix in {"xlsx", "xls"}:
        df = pd.read_excel(uploaded)

    else:
        df = pd.read_json(uploaded)

    summary = summarize_sales(df)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Rows", summary.rows)
    c2.metric("Total Sales", f"{summary.total_sales:,.2f}")
    c3.metric("Average Sales", f"{summary.average_sales:,.2f}")
    c4.metric("Max Sales", f"{summary.max_sales:,.2f}")

    st.subheader("Monthly Sales")

    monthly = sales_by_month(df)

    st.line_chart(monthly.set_index("month"))

    st.subheader("Month-over-Month Growth")

    st.dataframe(
        month_over_month_growth(df),
        use_container_width=True,
    )

    normalized = [
        str(c)
        .strip()
        .lower()
        .replace(" ", "_")
        .replace("-", "_")
        for c in df.columns
    ]

    for dimension in ["region", "product"]:
        if dimension in normalized:
            st.subheader(f"Sales by {dimension.title()}")

            result = sales_by_dimension(df, dimension)

            st.bar_chart(result.set_index(dimension))

    st.subheader("Simple Forecast")

    periods = st.slider(
        "Forecast periods",
        1,
        12,
        3,
    )

    st.dataframe(
        moving_average_forecast(
            df,
            periods=periods,
        ),
        use_container_width=True,
    )

else:
    st.info(
        "Upload a sales file with at least "
        "order_date and sales columns."
    )
