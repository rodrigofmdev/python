SELECT
    d.year,
    d.month,
    d.month_name,
    COUNT(DISTINCT f.order_id) AS order_count,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.sales_amount), 2) AS total_sales
FROM fact_sales AS f
JOIN dim_date AS d
    ON d.date_key = f.date_key
WHERE d.year = (SELECT MAX(year) FROM dim_date)
GROUP BY d.year, d.month, d.month_name
ORDER BY d.year, d.month;
