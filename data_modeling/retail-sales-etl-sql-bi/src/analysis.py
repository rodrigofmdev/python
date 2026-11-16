import sqlite3
from pathlib import Path

import pandas as pd

QUERY_FILES = {
    "sales_summary": "sales_summary.sql",
    "sales_by_category": "sales_by_category.sql",
    "sales_by_state": "sales_by_state.sql",
    "monthly_sales": "monthly_sales.sql",
}
MODEL_TABLES = (
    "dim_customer",
    "dim_product",
    "dim_date",
    "fact_sales",
)


def run_sql_reports(
    connection: sqlite3.Connection,
    sql_dir: Path,
) -> dict[str, pd.DataFrame]:
    """Execute the project's SQL reports and return their result tables."""

    reports = {}
    for report_name, query_file in QUERY_FILES.items():
        query = (sql_dir / query_file).read_text(encoding="utf-8")
        reports[report_name] = pd.read_sql_query(query, connection)
    return reports


def export_model_tables(
    connection: sqlite3.Connection,
    output_dir: Path,
) -> dict[str, pd.DataFrame]:
    """Export star-schema tables for Power BI and other BI tools."""

    model_tables = {}
    for table_name in MODEL_TABLES:
        table = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)
        model_tables[table_name] = table
        table.to_csv(
            output_dir / f"{table_name}.csv",
            index=False,
            encoding="utf-8-sig",
        )
    return model_tables


def export_sql_reports(
    reports: dict[str, pd.DataFrame],
    output_dir: Path,
) -> None:
    for report_name, report_data in reports.items():
        report_data.to_csv(
            output_dir / f"{report_name}.csv",
            index=False,
            encoding="utf-8-sig",
        )
