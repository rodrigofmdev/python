import calendar
import sqlite3
from pathlib import Path

import pandas as pd

REQUIRED_COLUMNS = (
    "sale_line_id",
    "order_id",
    "order_date",
    "customer_id",
    "customer_name",
    "city",
    "state",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
)
TEXT_COLUMNS = (
    "sale_line_id",
    "order_id",
    "customer_id",
    "customer_name",
    "city",
    "state",
    "product_id",
    "product_name",
    "category",
)


def read_sales_file(input_path: Path) -> pd.DataFrame:
    """Read sales from a CSV or Excel workbook."""

    suffix = input_path.suffix.casefold()
    if suffix == ".csv":
        return pd.read_csv(input_path)
    if suffix in (".xlsx", ".xlsm"):
        return pd.read_excel(input_path)
    raise ValueError("Input file must have a .csv, .xlsx, or .xlsm extension.")


def clean_sales_data(data: pd.DataFrame) -> pd.DataFrame:
    """Validate, clean, and enrich raw sales data."""

    missing_columns = set(REQUIRED_COLUMNS) - set(data.columns)
    if missing_columns:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing_columns))}"
        )

    cleaned = data.loc[:, list(REQUIRED_COLUMNS)].copy()

    for column in TEXT_COLUMNS:
        cleaned[column] = cleaned[column].astype("string").str.strip()
        cleaned[column] = cleaned[column].replace("", pd.NA)

    cleaned["order_date"] = pd.to_datetime(
        cleaned["order_date"],
        errors="coerce",
    )
    cleaned["quantity"] = pd.to_numeric(
        cleaned["quantity"],
        errors="coerce",
    )
    cleaned["unit_price"] = pd.to_numeric(
        cleaned["unit_price"],
        errors="coerce",
    )

    cleaned = cleaned.dropna(subset=list(REQUIRED_COLUMNS))
    cleaned = cleaned.drop_duplicates(subset=["sale_line_id"], keep="first")
    cleaned = cleaned[
        (cleaned["quantity"] > 0)
        & (cleaned["quantity"] % 1 == 0)
        & (cleaned["unit_price"] >= 0)
    ]

    cleaned["quantity"] = cleaned["quantity"].astype(int)
    cleaned["sales_amount"] = (
        cleaned["quantity"] * cleaned["unit_price"]
    ).round(2)
    cleaned["order_date"] = cleaned["order_date"].dt.strftime("%Y-%m-%d")

    if cleaned.empty:
        raise ValueError("No valid sales records remain after data cleaning.")

    return cleaned.reset_index(drop=True)


def load_star_schema(
    sales: pd.DataFrame,
    database_path: Path,
    schema_path: Path,
) -> sqlite3.Connection:
    """Load cleaned sales into a SQLite star schema."""

    connection = sqlite3.connect(database_path)
    keep_connection_open = False
    try:
        connection.execute("PRAGMA foreign_keys = ON")
        connection.executescript(schema_path.read_text(encoding="utf-8"))

        for row in sales.itertuples(index=False):
            connection.execute(
                """
                INSERT OR IGNORE INTO dim_customer
                    (customer_id, customer_name, city, state)
                VALUES (?, ?, ?, ?)
                """,
                (row.customer_id, row.customer_name, row.city, row.state),
            )
            customer_key = connection.execute(
                "SELECT customer_key FROM dim_customer WHERE customer_id = ?",
                (row.customer_id,),
            ).fetchone()[0]

            connection.execute(
                """
                INSERT OR IGNORE INTO dim_product
                    (product_id, product_name, category)
                VALUES (?, ?, ?)
                """,
                (row.product_id, row.product_name, row.category),
            )
            product_key = connection.execute(
                "SELECT product_key FROM dim_product WHERE product_id = ?",
                (row.product_id,),
            ).fetchone()[0]

            order_date = pd.Timestamp(row.order_date)
            date_key = int(order_date.strftime("%Y%m%d"))
            connection.execute(
                """
                INSERT OR IGNORE INTO dim_date
                    (date_key, calendar_date, year, quarter, month, month_name)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    date_key,
                    order_date.strftime("%Y-%m-%d"),
                    order_date.year,
                    (order_date.month - 1) // 3 + 1,
                    order_date.month,
                    calendar.month_name[order_date.month],
                ),
            )

            connection.execute(
                """
                INSERT INTO fact_sales
                    (
                        sale_line_id, order_id, customer_key, product_key,
                        date_key, quantity, unit_price, sales_amount
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    row.sale_line_id,
                    row.order_id,
                    customer_key,
                    product_key,
                    date_key,
                    int(row.quantity),
                    float(row.unit_price),
                    float(row.sales_amount),
                ),
            )

        connection.commit()
        keep_connection_open = True
        return connection
    finally:
        if not keep_connection_open:
            connection.close()
