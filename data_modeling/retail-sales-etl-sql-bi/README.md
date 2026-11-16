# Retail Sales ETL, SQL, and BI

## 🎯 Objective

Build an end-to-end sales analytics pipeline that extracts local CSV or Excel
files, cleans and validates them with Pandas, loads a relational star schema
in SQLite, and produces tables that can be explored in Power BI. The project
does not currently extract data directly from APIs or remote databases.

An optional ChatGPT-powered summary demonstrates how an LLM can interpret
aggregated results without sending customer-level data.

## ✨ Features

- Read sales data from CSV or Excel (`.xlsx`).
- Remove duplicate records and reject invalid dates, quantities, and prices.
- Load a relational model with customer, product, date, and sales fact tables.
- Demonstrate SQL `JOIN`, `WHERE`, `GROUP BY`, and aggregate functions.
- Export SQL results, model tables, an Excel workbook, and a Markdown report.
- Generate a dedicated multi-sheet workbook containing the Power BI model.
- Optionally generate a summary from aggregated data with the OpenAI API.
- Save each run in a timestamped output folder.

## 📂 Project Structure

- `main.py`: command-line interface and pipeline orchestration.
- `src/etl.py`: input loading, Pandas transformations, and SQLite loading.
- `src/analysis.py`: execute SQL reports and export model tables.
- `src/report.py`: Markdown and Excel report generation.
- `src/llm.py`: optional OpenAI summary from aggregated metrics.
- `sql/schema.sql`: relational star schema.
- `sql/`: analytical SQL queries.
- `data/raw/sales.csv`: fictional source data with sample quality issues.
- `POWER_BI_README.md`: data model, import, and DAX measure instructions.
- `tests/`: focused data-cleaning and relational-load tests.
- `output/`: timestamped database and analysis artifacts.

## 🧱 Data Model

The SQLite database uses a simple star schema:

- `fact_sales`: one row per order line, with quantity, unit price, and sales
  amount.
- `dim_customer`: customer attributes.
- `dim_product`: product and category attributes.
- `dim_date`: calendar attributes.

The analytical queries join the fact table to dimensions, apply date or region
filters, and aggregate sales and order counts for the latest year in the
loaded dataset.

## 🚀 How to Run

### 1. Navigate to the project folder

From the repository root, run:

```powershell
cd .\python\data_modeling\retail-sales-etl-sql-bi
```

### 2. Install dependencies

```powershell
py -3.15 -m pip install -r requirements.txt
```

### 3. Run the ETL and SQL analysis

```powershell
py -3.15 .\main.py
```

To load an Excel workbook instead of the sample CSV:

```powershell
py -3.15 .\main.py --input .\data\raw\sales.xlsx
```

### 4. Optional: generate an AI summary

Set your OpenAI API key in the same PowerShell terminal:

```powershell
$env:OPENAI_API_KEY = "paste-your-api-key-here"
```

Then run the pipeline with aggregated-data insights:

```powershell
py -3.15 .\main.py --ai-insights
```

The environment variable applies only to the current terminal session. Set it
again in a new terminal. Do not share your API key or commit it to the
repository. API usage may incur charges.

### Run the tests

```powershell
py -3.15 -m unittest discover -s .\tests
```

## 📊 Power BI

Follow [the Power BI setup guide](./POWER_BI_README.md) to import the exported
dimension and fact tables, create relationships, and add example DAX measures.

## 📄 Results

Each run creates `output/YYYY-MM-DD-HH-MM-SS/` with:

- `sales.db`: relational SQLite database.
- `dim_customer.csv`, `dim_product.csv`, `dim_date.csv`, and `fact_sales.csv`:
  model tables for BI.
- `sales_summary.csv`, `sales_by_category.csv`, `sales_by_state.csv`, and
  `monthly_sales.csv`: SQL aggregation results.
- `sales_analysis.xlsx`: multi-sheet workbook with the generated tables.
- `powerbi_model.xlsx`: fact and dimension tables in separate sheets, ready to
  import into Power BI.
- `report.md`: pipeline summary and analysis.

## 🔒 Data and Limitations

The included source data is fictional and intended for portfolio
demonstrations. The LLM option sends only aggregated query results to OpenAI;
it does not send source rows or customer names.

## ✍️ Author

@rodrigofmdev

- Email: rodrigofmdev@gmail.com
- GitHub: [github.com/rodrigofmdev](https://github.com/rodrigofmdev)
- LinkedIn: [linkedin.com/in/rodrigofmdev](https://linkedin.com/in/rodrigofmdev)
