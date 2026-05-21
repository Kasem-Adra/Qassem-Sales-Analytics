from __future__ import annotations

from pathlib import Path
import pandas as pd

from salesanalytics.core import sales_by_month, summarize_sales, top_items
from salesanalytics.kpis import month_over_month_growth


def build_html_report(df: pd.DataFrame, output: str | Path) -> Path:
    """Build a standalone HTML sales report."""
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    summary = summarize_sales(df)
    monthly = sales_by_month(df)
    growth = month_over_month_growth(df)

    sections = [
        "<h1>Qassem Sales Analytics Report</h1>",
        "<h2>Executive Summary</h2>",
        f"<p><strong>Total sales:</strong> {summary.total_sales:,.2f}</p>",
        f"<p><strong>Average sales:</strong> {summary.average_sales:,.2f}</p>",
        f"<p><strong>Rows analyzed:</strong> {summary.rows}</p>",
        "<h2>Monthly Sales</h2>",
        monthly.to_html(index=False),
        "<h2>Month-over-Month Growth</h2>",
        growth.to_html(index=False),
    ]

    normalized_columns = [str(c).lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    if "product" in normalized_columns:
        sections.extend(["<h2>Top Products</h2>", top_items(df, "product").to_html(index=False)])
    if "region" in normalized_columns:
        sections.extend(["<h2>Top Regions</h2>", top_items(df, "region").to_html(index=False)])

    html = f"""<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Qassem Sales Analytics Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }}
    h1 {{ color: #111827; }}
    h2 {{ border-bottom: 1px solid #ddd; padding-bottom: 6px; }}
    table {{ border-collapse: collapse; width: 100%; margin: 16px 0; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f3f4f6; }}
  </style>
</head>
<body>
{''.join(sections)}
</body>
</html>"""
    output_path.write_text(html, encoding="utf-8")
    return output_path
