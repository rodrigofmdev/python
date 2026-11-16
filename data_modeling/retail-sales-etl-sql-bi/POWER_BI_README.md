# Power BI Setup

## Import the data

Run the Python pipeline first. The latest `output/YYYY-MM-DD-HH-MM-SS` folder
contains both individual CSV files and a `powerbi_model.xlsx` workbook with one
sheet per model table. In Power BI Desktop, select **Get Data > Excel workbook**
and load the four model sheets from that workbook, or import these CSVs:

- `fact_sales.csv`
- `dim_customer.csv`
- `dim_product.csv`
- `dim_date.csv`

## Create the relationships

In **Model view**, create these one-to-many relationships with single-direction
filtering from each dimension to the fact table:

- `dim_customer[customer_key]` → `fact_sales[customer_key]`
- `dim_product[product_key]` → `fact_sales[product_key]`
- `dim_date[date_key]` → `fact_sales[date_key]`

Mark `dim_date` as the date table using `dim_date[calendar_date]`.

## Add example DAX measures

```DAX
Total Sales = SUM(fact_sales[sales_amount])

Orders = DISTINCTCOUNT(fact_sales[order_id])

Units Sold = SUM(fact_sales[quantity])

Average Order Value = DIVIDE([Total Sales], [Orders])
```

## Suggested report visuals

- Card visuals for Total Sales, Orders, and Average Order Value.
- A line chart using `dim_date[calendar_date]` and Total Sales.
- A bar chart for Total Sales by `dim_product[category]`.
- A map or bar chart for Total Sales by `dim_customer[state]`.
- Slicers for year, category, and state.
