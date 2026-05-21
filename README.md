# Qassem Sales Analytics

[![Tests](https://github.com/Kasem-Adra/Qassem-Sales-Analytics/actions/workflows/tests.yml/badge.svg)](https://github.com/Kasem-Adra/Qassem-Sales-Analytics/actions/workflows/tests.yml)
[![Docker Build](https://github.com/Kasem-Adra/Qassem-Sales-Analytics/actions/workflows/docker.yml/badge.svg)](https://github.com/Kasem-Adra/Qassem-Sales-Analytics/actions/workflows/docker.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

Enterprise-grade sales analytics toolkit by **Kasem Adra** under the **Qassem** brand.

## Overview

**Qassem Sales Analytics** is a professional Python analytics toolkit for sales reporting, KPI tracking, forecasting, and interactive dashboard workflows.

> Repository: `Qassem-Sales-Analytics`  
> CLI command: `qsales`  
> Dashboard: Streamlit app

## Key Capabilities

- Sales summary analytics
- Monthly revenue aggregation
- Top products, regions, and channels
- Month-over-month growth
- Revenue contribution analysis
- Simple moving-average forecasting
- Standalone HTML report generation
- Streamlit dashboard
- Docker-ready
- GitHub Actions CI
- Unit tests
- Professional package structure

## Installation

```bash
git clone https://github.com/Kasem-Adra/Qassem-Sales-Analytics.git
cd Qassem-Sales-Analytics
python -m pip install -e .
```

## CLI Usage

```bash
qsales summary examples/sample_sales.csv
qsales monthly examples/sample_sales.csv
qsales by examples/sample_sales.csv region
qsales top examples/sample_sales.csv product --limit 5
qsales growth examples/sample_sales.csv
qsales contribution examples/sample_sales.csv region
qsales forecast examples/sample_sales.csv --periods 6
qsales report examples/sample_sales.csv --output reports/sales_report.html
```

## Dashboard

```bash
streamlit run salesanalytics/dashboard/app.py
```

## Docker

```bash
docker build -t qassem-sales-analytics .
docker run --rm qassem-sales-analytics --help
```

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

## Expected Data Format

Required columns:

```text
order_date,sales
```

Recommended columns:

```text
region,product,channel,customer
```

Column names are normalized automatically, so `Order Date` becomes `order_date`.

## Project Structure

```text
Qassem-Sales-Analytics/
├── salesanalytics/
│   ├── core.py
│   ├── kpis.py
│   ├── cli.py
│   ├── ml/
│   ├── reporting/
│   └── dashboard/
├── tests/
├── docs/
├── examples/
├── reports/
├── legacy/
├── Dockerfile
├── pyproject.toml
├── LICENSE
└── README.md
```

## License

This project is licensed under the MIT License.
