SELECT
    p.category,
    COUNT(DISTINCT f.order_id) AS order_count,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.sales_amount), 2) AS total_sales,
    ROUND(AVG(f.sales_amount), 2) AS average_line_value
FROM fact_sales AS f
JOIN dim_product AS p
    ON p.product_key = f.product_key
JOIN dim_date AS d
    ON d.date_key = f.date_key
WHERE d.year = (SELECT MAX(year) FROM dim_date)
GROUP BY p.category
ORDER BY total_sales DESC;
