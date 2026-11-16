import sqlite3
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.etl import clean_sales_data, load_star_schema, read_sales_file

PROJECT_DIR = Path(__file__).resolve().parents[1]


class SalesEtlTests(unittest.TestCase):
    def test_cleaning_removes_duplicate_and_invalid_rows(self):
        source = read_sales_file(PROJECT_DIR / "data" / "raw" / "sales.csv")
        cleaned = clean_sales_data(source)

        self.assertEqual(len(source), 19)
        self.assertEqual(len(cleaned), 16)
        self.assertTrue(cleaned["sale_line_id"].is_unique)
        self.assertTrue((cleaned["quantity"] > 0).all())
        self.assertTrue((cleaned["sales_amount"] >= 0).all())

    def test_cleaning_rejects_missing_required_columns(self):
        with self.assertRaisesRegex(ValueError, "Missing required columns"):
            clean_sales_data(pd.DataFrame({"sale_line_id": ["SL001"]}))

    def test_excel_input_and_star_schema_load(self):
        source = read_sales_file(PROJECT_DIR / "data" / "raw" / "sales.csv")
        cleaned = clean_sales_data(source)

        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            workbook_path = temporary_path / "source.xlsx"
            cleaned.to_excel(workbook_path, index=False)
            reloaded = read_sales_file(workbook_path)
            self.assertEqual(len(reloaded), len(cleaned))

            connection = load_star_schema(
                cleaned,
                temporary_path / "sales.db",
                PROJECT_DIR / "sql" / "schema.sql",
            )
            try:
                fact_count = connection.execute(
                    "SELECT COUNT(*) FROM fact_sales"
                ).fetchone()[0]
                foreign_key_errors = connection.execute(
                    "PRAGMA foreign_key_check"
                ).fetchall()
            finally:
                connection.close()

        self.assertEqual(fact_count, 16)
        self.assertEqual(foreign_key_errors, [])


if __name__ == "__main__":
    unittest.main()
