#!/usr/bin/env bash
set -e

qsales summary examples/sample_sales.csv
qsales monthly examples/sample_sales.csv
