SELECT
    c.state,
    COUNT(DISTINCT f.order_id) AS order_count,
    SUM(f.quantity) AS units_sold,
    ROUND(SUM(f.sales_amount), 2) AS total_sales
FROM fact_sales AS f
JOIN dim_customer AS c
    ON c.customer_key = f.customer_key
JOIN dim_date AS d
    ON d.date_key = f.date_key
WHERE c.state IN ('SP', 'RJ', 'MG', 'PR', 'RS')
  AND d.year = (SELECT MAX(year) FROM dim_date)
GROUP BY c.state
ORDER BY total_sales DESC;
