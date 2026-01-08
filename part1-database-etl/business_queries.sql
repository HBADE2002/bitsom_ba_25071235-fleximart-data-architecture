-- Query 1: Customer Purchase History
-- Business Question: Generate a detailed report showing each customer's name, email, total number of orders placed, and total amount spent. Include only customers who have placed at least 2 orders and spent more than ₹5,000. Order by total amount spent in descending order.
-- Expected to return customers with 2+ orders and >5000 spent

SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    c.email,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount::NUMERIC) AS total_spent
FROM customers c
JOIN orders o 
    ON c.customer_id = o.customer_id
GROUP BY 
    c.first_name, 
    c.last_name, 
    c.email
HAVING 
    COUNT(o.order_id) >= 2
    AND SUM(o.total_amount::NUMERIC) > 5000
ORDER BY 
    total_spent DESC;


-- Query 2: Product Sales Analysis
-- Business Question: For each product category, show the category name, number of different products sold, total quantity sold, and total revenue generated. Only include categories that have generated more than ₹10,000 in revenue. Order by total revenue descending.
-- Expected to return categories with >10000 revenue

SELECT
    p.category,
    COUNT(DISTINCT p.product_id) AS num_products,
    SUM(oi.quantity::INT) AS total_quantity_sold,
    SUM(oi.subtotal::NUMERIC) AS total_revenue
FROM products p
JOIN order_items oi
    ON p.product_id = oi.product_id
GROUP BY
    p.category
HAVING
    SUM(oi.subtotal::NUMERIC) > 10000
ORDER BY
    total_revenue DESC;


-- Query 3: Monthly Sales Trend
-- Business Question: Show monthly sales trends for the year 2024. For each month, display the month name, total number of orders, total revenue, and the running total of revenue (cumulative revenue from January to that month).
-- Expected to show monthly and cumulative revenue

SELECT
    TO_CHAR(order_month, 'Month') AS month_name,
    total_orders,
    monthly_revenue,
    SUM(monthly_revenue) OVER (ORDER BY order_month) AS cumulative_revenue
FROM (
    SELECT
        DATE_TRUNC('month', order_date::DATE) AS order_month,
        COUNT(order_id) AS total_orders,
        SUM(total_amount::NUMERIC) AS monthly_revenue
    FROM orders
    WHERE EXTRACT(YEAR FROM order_date::DATE) = 2024
    GROUP BY DATE_TRUNC('month', order_date::DATE)
) monthly_data
ORDER BY order_month;


