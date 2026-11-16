import argparse
import os
import sqlite3
import time
from datetime import datetime
from pathlib import Path

from src.analysis import export_model_tables, export_sql_reports, run_sql_reports
from src.etl import clean_sales_data, load_star_schema, read_sales_file
from src.llm import generate_ai_insights
from src.report import (
    generate_excel_workbook,
    generate_markdown_report,
    generate_powerbi_workbook,
)

BASE_DIR = Path(__file__).parent
DEFAULT_INPUT = BASE_DIR / "data" / "raw" / "sales.csv"
OUTPUT_DIR = BASE_DIR / "output"
SCHEMA_FILE = BASE_DIR / "sql" / "schema.sql"
SQL_DIR = BASE_DIR / "sql"


def create_run_output_dir() -> Path:
    """Create a unique output folder named with the current timestamp."""

    OUTPUT_DIR.mkdir(exist_ok=True)

    while True:
        run_output_dir = OUTPUT_DIR / datetime.now().strftime(
            "%Y-%m-%d-%H-%M-%S"
        )

        try:
            run_output_dir.mkdir()
        except FileExistsError:
            time.sleep(1)
        else:
            return run_output_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run retail sales ETL, SQL analytics, and BI exports."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help="Path to a source CSV or Excel workbook.",
    )
    parser.add_argument(
        "--ai-insights",
        action="store_true",
        help="Add an AI-generated summary from aggregated sales data.",
    )
    args = parser.parse_args()

    if args.ai_insights and not os.getenv("OPENAI_API_KEY"):
        raise SystemExit(
            "Set OPENAI_API_KEY to use --ai-insights."
        )

    input_path = Path(args.input)
    raw_sales = read_sales_file(input_path)
    cleaned_sales = clean_sales_data(raw_sales)
    run_output_dir = create_run_output_dir()
    database_path = run_output_dir / "sales.db"

    connection = load_star_schema(
        cleaned_sales,
        database_path,
        SCHEMA_FILE,
    )
    try:
        reports = run_sql_reports(connection, SQL_DIR)
        model_tables = export_model_tables(connection, run_output_dir)
    finally:
        connection.close()

    export_sql_reports(reports, run_output_dir)
    generate_excel_workbook(
        cleaned_sales,
        reports,
        run_output_dir / "sales_analysis.xlsx",
    )
    generate_powerbi_workbook(
        model_tables,
        run_output_dir / "powerbi_model.xlsx",
    )

    ai_insights = None
    if args.ai_insights:
        ai_insights = generate_ai_insights(
            reports["sales_by_category"],
            reports["sales_by_state"],
        )

    generate_markdown_report(
        len(raw_sales),
        len(cleaned_sales),
        reports,
        run_output_dir / "report.md",
        ai_insights,
    )

    relative_output_path = run_output_dir.relative_to(BASE_DIR)
    print(
        f"Analysis complete. Generated files in: "
        f"{relative_output_path}{os.sep}"
    )


if __name__ == "__main__":
    main()
