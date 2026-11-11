-- SQLite examples. Run after importing rows into a table named sales.
-- Revenue and profit use the starter definition: quantity * price/cost.

-- 1. Overall totals
SELECT
    SUM(quantity * unit_price) AS total_revenue,
    SUM(quantity * (unit_price - unit_cost)) AS total_profit,
    SUM(quantity) AS units_sold
FROM sales;

-- 2. Revenue and profit by region
SELECT
    region,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales
GROUP BY region
ORDER BY revenue DESC;

-- 3. Monthly trend (SQLite strftime extracts year-month)
SELECT
    strftime('%Y-%m', order_date) AS sales_month,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales
GROUP BY sales_month
ORDER BY sales_month;

-- 4. Product performance
SELECT
    product_name,
    SUM(quantity) AS units_sold,
    SUM(quantity * unit_price) AS revenue,
    SUM(quantity * (unit_price - unit_cost)) AS profit
FROM sales
GROUP BY product_name
ORDER BY profit DESC;

-- 5. CTE example: calculate revenue first, then aggregate by category
WITH order_lines AS (
    SELECT category, quantity * unit_price AS revenue
    FROM sales
)
SELECT category, SUM(revenue) AS revenue
FROM order_lines
GROUP BY category
ORDER BY revenue DESC;
