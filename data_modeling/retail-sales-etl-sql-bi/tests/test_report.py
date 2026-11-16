import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.report import generate_markdown_report, generate_powerbi_workbook


class PortugueseReportTests(unittest.TestCase):
    def test_report_uses_brazilian_portuguese_and_currency_format(self):
        reports = {
            "sales_summary": pd.DataFrame(
                [
                    {
                        "order_count": 2,
                        "units_sold": 3,
                        "total_sales": 1234.5,
                        "average_order_value": 617.25,
                    }
                ]
            ),
            "sales_by_category": pd.DataFrame(
                [
                    {
                        "category": "Electronics",
                        "order_count": 2,
                        "units_sold": 3,
                        "total_sales": 1234.5,
                        "average_line_value": 617.25,
                    }
                ]
            ),
            "sales_by_state": pd.DataFrame(
                [
                    {
                        "state": "SP",
                        "order_count": 2,
                        "units_sold": 3,
                        "total_sales": 1234.5,
                    }
                ]
            ),
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            report_path = Path(temporary_directory) / "report.md"
            generate_markdown_report(3, 2, reports, report_path)
            report = report_path.read_text(encoding="utf-8")

        self.assertIn("# Análise de Vendas no Varejo", report)
        self.assertIn("Vendas totais: R$ 1.234,50", report)
        self.assertIn("Eletrônicos", report)
        self.assertIn("Vendas por estado", report)
        self.assertNotIn("Sales by category", report)

    def test_powerbi_workbook_contains_star_schema_tables(self):
        model_tables = {
            "dim_customer": pd.DataFrame([{"customer_key": 1}]),
            "dim_product": pd.DataFrame([{"product_key": 1}]),
            "dim_date": pd.DataFrame([{"date_key": 20250101}]),
            "fact_sales": pd.DataFrame([{"sale_line_id": "SL001"}]),
        }

        with tempfile.TemporaryDirectory() as temporary_directory:
            workbook_path = Path(temporary_directory) / "powerbi_model.xlsx"
            generate_powerbi_workbook(model_tables, workbook_path)
            with pd.ExcelFile(workbook_path) as workbook:
                sheet_names = set(workbook.sheet_names)

        self.assertEqual(
            sheet_names,
            set(model_tables),
        )


if __name__ == "__main__":
    unittest.main()
