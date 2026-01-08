import pandas as pd
import psycopg2
from dateutil import parser
import re
import os

# ===================== DATABASE CONFIG =====================
POSTGRES_CONFIG = {
    "dbname": "fleximart",
    "user": "postgres",
    "password": "abhi1310@",
    "host": "localhost",
    "port": "5433"
}

# ===================== DATA QUALITY TRACKER =====================
dq_metrics = {
    "customers": {"total": 0, "duplicates": 0, "missing_pk": 0, "inserted": 0},
    "products": {"total": 0, "duplicates": 0, "missing_pk": 0, "inserted": 0},
    "sales": {"total": 0, "duplicates": 0, "missing_pk": 0, "inserted": 0}
}

# ===================== UTILITY FUNCTIONS =====================
def normalize_phone(value):
    if pd.isna(value):
        return "N/A"

    digits = re.sub(r"\D", "", str(value))

    if digits.startswith("91") and len(digits) > 10:
        digits = digits[-10:]
    elif digits.startswith("0") and len(digits) > 10:
        digits = digits[-10:]

    return "+91-" + digits if len(digits) == 10 else "N/A"


def normalize_date(value):
    try:
        return parser.parse(str(value)).strftime("%Y-%m-%d")
    except Exception:
        return "N/A"


def clean_string(value):
    return "N/A" if pd.isna(value) else str(value).strip()


def format_title(value):
    return "N/A" if pd.isna(value) else str(value).strip().title()


# ===================== DB CONNECTION =====================
connection = psycopg2.connect(**POSTGRES_CONFIG)
cursor = connection.cursor()

# ===================== TABLE CREATION =====================
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customers_serialno SERIAL,
    customer_id VARCHAR(10) PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    city VARCHAR(50),
    registration_date VARCHAR(20)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    products_serialno SERIAL,
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price VARCHAR(20),
    stock_quantity VARCHAR(20)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    orders_serialno SERIAL,
    order_id VARCHAR(10) PRIMARY KEY,
    customer_id VARCHAR(10),
    order_date VARCHAR(20),
    total_amount VARCHAR(20),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS order_items (
    order_items_serialno SERIAL,
    order_id VARCHAR(10),
    product_id VARCHAR(10),
    quantity VARCHAR(20),
    unit_price VARCHAR(20),
    subtotal VARCHAR(20),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")

connection.commit()

# ==========================================================
# ===================== CUSTOMERS LOAD =====================
# ==========================================================
cust_df = pd.read_csv("customers_raw.csv")
dq_metrics["customers"]["total"] = len(cust_df)

before = len(cust_df)
cust_df = cust_df[cust_df["customer_id"].notna()]
dq_metrics["customers"]["missing_pk"] = before - len(cust_df)

before = len(cust_df)
cust_df.drop_duplicates(subset="customer_id", inplace=True)
dq_metrics["customers"]["duplicates"] = before - len(cust_df)

cust_df["email"] = cust_df["email"].fillna("N/A")
cust_df["phone"] = cust_df["phone"].apply(normalize_phone)
cust_df["city"] = cust_df["city"].apply(format_title)
cust_df["registration_date"] = cust_df["registration_date"].apply(normalize_date)

for _, row in cust_df.iterrows():
    cursor.execute("""
        INSERT INTO customers
        (customer_id, first_name, last_name, email, phone, city, registration_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (customer_id) DO NOTHING
    """, tuple(row))

    if cursor.rowcount == 1:
        dq_metrics["customers"]["inserted"] += 1

connection.commit()

# ==========================================================
# ===================== PRODUCTS LOAD ======================
# ==========================================================
prod_df = pd.read_csv("products_raw.csv")
dq_metrics["products"]["total"] = len(prod_df)

before = len(prod_df)
prod_df = prod_df[prod_df["product_id"].notna()]
dq_metrics["products"]["missing_pk"] = before - len(prod_df)

before = len(prod_df)
prod_df.drop_duplicates(subset="product_id", inplace=True)
dq_metrics["products"]["duplicates"] = before - len(prod_df)

prod_df["product_name"] = prod_df["product_name"].apply(clean_string)
prod_df["category"] = prod_df["category"].apply(format_title)
prod_df["price"] = prod_df["price"].fillna("N/A")
prod_df["stock_quantity"] = prod_df["stock_quantity"].fillna("N/A")

for _, row in prod_df.iterrows():
    cursor.execute("""
        INSERT INTO products
        (product_id, product_name, category, price, stock_quantity)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (product_id) DO NOTHING
    """, tuple(row))

    if cursor.rowcount == 1:
        dq_metrics["products"]["inserted"] += 1

connection.commit()

# ==========================================================
# ===================== SALES LOAD =========================
# ==========================================================
sales_df = pd.read_csv("sales_raw.csv")
dq_metrics["sales"]["total"] = len(sales_df)

before = len(sales_df)
sales_df = sales_df[sales_df["transaction_id"].notna()]
dq_metrics["sales"]["missing_pk"] = before - len(sales_df)

before = len(sales_df)
sales_df.drop_duplicates(subset="transaction_id", inplace=True)
dq_metrics["sales"]["duplicates"] = before - len(sales_df)

sales_df["transaction_date"] = sales_df["transaction_date"].apply(normalize_date)

valid_customer_ids = set(pd.read_sql("SELECT customer_id FROM customers", connection)["customer_id"])
valid_product_ids = set(pd.read_sql("SELECT product_id FROM products", connection)["product_id"])

for _, row in sales_df.iterrows():

    if row["customer_id"] not in valid_customer_ids or row["product_id"] not in valid_product_ids:
        continue

    order_total = float(row["quantity"]) * float(row["unit_price"])

    cursor.execute("""
        INSERT INTO orders
        (order_id, customer_id, order_date, total_amount, status)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (order_id) DO NOTHING
    """, (
        row["transaction_id"],
        row["customer_id"],
        row["transaction_date"],
        str(order_total),
        row["status"]
    ))

    if cursor.rowcount == 1:
        cursor.execute("""
            INSERT INTO order_items
            (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            row["transaction_id"],
            row["product_id"],
            row["quantity"],
            row["unit_price"],
            str(order_total)
        ))

        dq_metrics["sales"]["inserted"] += 1

connection.commit()

# ==========================================================
# ===================== QUALITY REPORT =====================
# ==========================================================
with open("data_quality_report.txt", "w") as file:
    for table, stats in dq_metrics.items():
        file.write(f"{table.upper()} DATA\n")
        file.write(f"Records processed: {stats['total']}\n")
        file.write(f"Duplicate records removed: {stats['duplicates']}\n")
        file.write(f"Rows with missing PK: {stats['missing_pk']}\n")
        file.write(f"Records inserted: {stats['inserted']}\n\n")

cursor.close()
connection.close()

print("ETL pipeline executed successfully")
print("Data quality report generated")
