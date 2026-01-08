-- Customer Purchase Summary
-- Customers with 2+ orders and total spend above ₹5,000

SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS full_name,
    c.email AS customer_email,
    COUNT(o.order_id) AS order_count,
    SUM(o.total_amount::NUMERIC) AS amount_spent
FROM customers AS c
INNER JOIN orders AS o
    ON o.customer_id = c.customer_id
GROUP BY
    CONCAT(c.first_name, ' ', c.last_name),
    c.email
HAVING
    COUNT(o.order_id) >= 2
    AND SUM(o.total_amount::NUMERIC) > 5000
ORDER BY
    amount_spent DESC;


-- Category-wise Sales Performance
-- Categories generating more than ₹10,000 revenue

SELECT
    p.category AS category_name,
    COUNT(DISTINCT p.product_id) AS products_sold_count,
    SUM(oi.quantity::INT) AS units_sold,
    SUM(oi.subtotal::NUMERIC) AS revenue_generated
FROM products AS p
INNER JOIN order_items AS oi
    ON oi.product_id = p.product_id
GROUP BY
    p.category
HAVING
    SUM(oi.subtotal::NUMERIC) > 10000
ORDER BY
    revenue_generated DESC;


-- Monthly Revenue Trend for 2024
-- Includes cumulative revenue

SELECT
    TO_CHAR(month_start, 'Month') AS sales_month,
    orders_in_month,
    revenue_in_month,
    SUM(revenue_in_month) OVER (ORDER BY month_start) AS running_revenue
FROM (
    SELECT
        DATE_TRUNC('month', order_date::DATE) AS month_start,
        COUNT(order_id) AS orders_in_month,
        SUM(total_amount::NUMERIC) AS revenue_in_month
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date::DATE) = 2024
    GROUP BY
        DATE_TRUNC('month', order_date::DATE)
) AS monthly_summary
ORDER BY
    month_start;



