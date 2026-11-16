SELECT
    COUNT(DISTINCT order_id) AS order_count,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales_amount), 2) AS total_sales,
    ROUND(
        SUM(f.sales_amount) / COUNT(DISTINCT f.order_id),
        2
    ) AS average_order_value
FROM fact_sales AS f
JOIN dim_date AS d
    ON d.date_key = f.date_key
WHERE d.year = (SELECT MAX(year) FROM dim_date);
