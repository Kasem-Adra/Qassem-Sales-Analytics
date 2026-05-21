# Usage Guide

## Summary

```bash
qsales summary examples/sample_sales.csv
```

## Monthly sales

```bash
qsales monthly examples/sample_sales.csv
```

## Sales by dimension

```bash
qsales by examples/sample_sales.csv region
qsales by examples/sample_sales.csv product
qsales by examples/sample_sales.csv channel
```

## Top contributors

```bash
qsales top examples/sample_sales.csv product --limit 5
```

## Growth

```bash
qsales growth examples/sample_sales.csv
```

## Forecasting

```bash
qsales forecast examples/sample_sales.csv --periods 6
```

## HTML Report

```bash
qsales report examples/sample_sales.csv --output reports/sales_report.html
```

## Dashboard

```bash
streamlit run salesanalytics/dashboard/app.py
```
