# Databricks Table Creation

Examples for creating tables in Databricks (Delta Lake / Unity Catalog).

## Contents

| Path | What it shows |
| --- | --- |
| `sql/01_create_schema_and_tables.sql` | Schema, managed Delta tables with identity columns, primary/foreign keys, CHECK constraints, partitioning, table properties, CTAS, external tables and `read_files` |
| `notebooks/create_tables_pyspark.py` | PySpark: table from an explicit schema, from a DataFrame, and with the `DeltaTable` builder |

## Usage

1. Import `notebooks/create_tables_pyspark.py` into your workspace (it is in Databricks notebook source format), or paste the SQL file into a SQL editor / notebook.
2. Change `main` / `sales` to your own catalog and schema.
3. Run on a Unity Catalog-enabled cluster or SQL warehouse.

## Notes

- Constraints such as primary and foreign keys are informational in Databricks; `NOT NULL` and `CHECK` are enforced.
- Commented-out external-table and CSV examples need your own storage path or volume.
