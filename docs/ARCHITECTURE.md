# Architecture

Qassem Sales Analytics is organized as a professional analytics product.

## Modules

- `salesanalytics.core`: loading, cleaning, validation, aggregation
- `salesanalytics.kpis`: growth and contribution KPIs
- `salesanalytics.ml.forecast`: simple forecasting
- `salesanalytics.reporting.html`: standalone HTML report generation
- `salesanalytics.dashboard.app`: Streamlit dashboard
- `salesanalytics.cli`: command-line interface

## Design Goals

- Safe public sample data
- Clear CLI
- Easy local development
- GitHub Actions compatible
- Docker compatible
- Future-ready for API and SaaS expansion
