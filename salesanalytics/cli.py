from __future__ import annotations

import argparse

from .core import (
    load_sales_data,
    sales_by_dimension,
    sales_by_month,
    summarize_sales,
    top_items,
)
from .kpis import month_over_month_growth, revenue_contribution
from .ml.forecast import moving_average_forecast
from .reporting.html import build_html_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="qsales",
        description="Qassem Sales Analytics - enterprise sales analytics CLI",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    summary = sub.add_parser("summary", help="Show sales summary.")
    summary.add_argument("file")

    monthly = sub.add_parser("monthly", help="Aggregate sales by month.")
    monthly.add_argument("file")
    monthly.add_argument("--output", "-o")

    dimension = sub.add_parser("by", help="Aggregate sales by dimension.")
    dimension.add_argument("file")
    dimension.add_argument("dimension")
    dimension.add_argument("--output", "-o")

    top = sub.add_parser("top", help="Show top items by dimension.")
    top.add_argument("file")
    top.add_argument("dimension")
    top.add_argument("--limit", type=int, default=10)

    growth = sub.add_parser("growth", help="Show month-over-month growth.")
    growth.add_argument("file")

    contribution = sub.add_parser(
        "contribution",
        help="Show revenue contribution by dimension.",
    )
    contribution.add_argument("file")
    contribution.add_argument("dimension")

    forecast = sub.add_parser(
        "forecast",
        help="Generate moving-average forecast.",
    )
    forecast.add_argument("file")
    forecast.add_argument("--periods", type=int, default=3)

    report = sub.add_parser(
        "report",
        help="Generate standalone HTML report.",
    )
    report.add_argument("file")
    report.add_argument(
        "--output",
        "-o",
        default="reports/sales_report.html",
    )

    sub.add_parser(
        "dashboard",
        help="Print command for launching Streamlit dashboard.",
    )

    return parser


def print_frame(df) -> None:
    print(df.to_string(index=False))


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "dashboard":
        print("Run: streamlit run salesanalytics/dashboard/app.py")
        return 0

    df = load_sales_data(args.file)

    if args.command == "summary":
        summary = summarize_sales(df)

        for key, value in summary.__dict__.items():
            if value is not None:
                print(f"{key}: {value}")

        return 0

    if args.command == "monthly":
        result = sales_by_month(df)

        if args.output:
            result.to_csv(args.output, index=False)
            print(f"saved: {args.output}")
        else:
            print_frame(result)

        return 0

    if args.command == "by":
        result = sales_by_dimension(df, args.dimension)

        if args.output:
            result.to_csv(args.output, index=False)
            print(f"saved: {args.output}")
        else:
            print_frame(result)

        return 0

    if args.command == "top":
        print_frame(
            top_items(
                df,
                args.dimension,
                limit=args.limit,
            )
        )
        return 0

    if args.command == "growth":
        print_frame(month_over_month_growth(df))
        return 0

    if args.command == "contribution":
        print_frame(revenue_contribution(df, args.dimension))
        return 0

    if args.command == "forecast":
        print_frame(
            moving_average_forecast(
                df,
                periods=args.periods,
            )
        )
        return 0

    if args.command == "report":
        path = build_html_report(df, args.output)
        print(f"saved: {path}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
