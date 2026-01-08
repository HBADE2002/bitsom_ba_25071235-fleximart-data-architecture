import pandas as pd
import psycopg2
from dateutil import parser
import re
import os

# ===================== DB CONFIG =====================
DB_CONFIG = {
    "dbname": "fleximart",
    "user": "postgres",
    "password": "abhi1310@",
    "host": "localhost",
    "port": "5433"
}

# ===================== DATA QUALITY METRICS =====================
report = {
    "customers": {"processed": 0, "duplicates": 0, "pk_missing": 0, "loaded": 0},
    "products": {"processed": 0, "duplicates": 0, "pk_missing": 0, "loaded": 0},
    "sales": {"processed": 0, "duplicates": 0, "pk_missing": 0, "loaded": 0}
}

# ===================== HELPERS =====================
def standardize_phone(phone):
    if pd.isna(phone):
        return "N/A"

    digits = re.sub(r"\D", "", str(phone))

    if digits.startswith("91") and len(digits) > 10:
        digits = digits[-10:]
    elif digits.startswith("0") and len(digits) > 10:
        digits = digits[-10:]

    if len(digits) < 10:
        return "N/A"

    return "+91-" + digits


def standardize_date(val):
    try:
        return parser.parse(str(val)).strftime("%Y-%m-%d")
    except:
        return "N/A"


def clean_text(val):
    if pd.isna(val):
        return "N/A"
    return str(val).strip()


def title_text(val):
    if pd.isna(val):
        return "N/A"
    return str(val).strip().title()


# ===================== CONNECT DB =====================
conn = psycopg2.connect(**DB_CONFIG)
cur = conn.cursor()

# ===================== CREATE TABLES =====================
cur.execute("""
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

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    products_serialno SERIAL,
    product_id VARCHAR(10) PRIMARY KEY,
    product_name VARCHAR(100),
    category VARCHAR(50),
    price VARCHAR(20),
    stock_quantity VARCHAR(20)
);
""")

cur.execute("""
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

cur.execute("""
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

conn.commit()

# =====================================================
# ===================== CUSTOMERS ETL =================
# =====================================================
df = pd.read_csv("customers_raw.csv")
report["customers"]["processed"] = len(df)

before = len(df)
df = df[df["customer_id"].notna()]
report["customers"]["pk_missing"] = before - len(df)

before = len(df)
df.drop_duplicates(subset="customer_id", inplace=True)
report["customers"]["duplicates"] = before - len(df)

df["email"] = df["email"].fillna("N/A")
df["phone"] = df["phone"].apply(standardize_phone)
df["city"] = df["city"].apply(title_text)
df["registration_date"] = df["registration_date"].apply(standardize_date)

for _, r in df.iterrows():
    cur.execute("""
        INSERT INTO customers
        (customer_id, first_name, last_name, email, phone, city, registration_date)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (customer_id) DO NOTHING
    """, tuple(r))

    if cur.rowcount == 1:
        report["customers"]["loaded"] += 1

conn.commit()

# =====================================================
# ===================== PRODUCTS ETL ==================
# =====================================================
df = pd.read_csv("products_raw.csv")
report["products"]["processed"] = len(df)

before = len(df)
df = df[df["product_id"].notna()]
report["products"]["pk_missing"] = before - len(df)

before = len(df)
df.drop_duplicates(subset="product_id", inplace=True)
report["products"]["duplicates"] = before - len(df)

df["product_name"] = df["product_name"].apply(clean_text)
df["category"] = df["category"].apply(title_text)
df["price"] = df["price"].fillna("N/A")
df["stock_quantity"] = df["stock_quantity"].fillna("N/A")

for _, r in df.iterrows():
    cur.execute("""
        INSERT INTO products
        (product_id, product_name, category, price, stock_quantity)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (product_id) DO NOTHING
    """, tuple(r))

    if cur.rowcount == 1:
        report["products"]["loaded"] += 1

conn.commit()

# =====================================================
# ===================== SALES ETL =====================
# =====================================================
df = pd.read_csv("sales_raw.csv")
report["sales"]["processed"] = len(df)

before = len(df)
df = df[df["transaction_id"].notna()]
report["sales"]["pk_missing"] = before - len(df)

before = len(df)
df.drop_duplicates(subset="transaction_id", inplace=True)
report["sales"]["duplicates"] = before - len(df)

df["transaction_date"] = df["transaction_date"].apply(standardize_date)

valid_customers = set(pd.read_sql("SELECT customer_id FROM customers", conn)["customer_id"])
valid_products = set(pd.read_sql("SELECT product_id FROM products", conn)["product_id"])

for _, r in df.iterrows():

    if r["customer_id"] not in valid_customers or r["product_id"] not in valid_products:
        continue

    total = float(r["quantity"]) * float(r["unit_price"])

    cur.execute("""
        INSERT INTO orders
        (order_id, customer_id, order_date, total_amount, status)
        VALUES (%s,%s,%s,%s,%s)
        ON CONFLICT (order_id) DO NOTHING
    """, (
        r["transaction_id"],
        r["customer_id"],
        r["transaction_date"],
        str(total),
        r["status"]
    ))

    if cur.rowcount == 1:
        cur.execute("""
            INSERT INTO order_items
            (order_id, product_id, quantity, unit_price, subtotal)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            r["transaction_id"],
            r["product_id"],
            r["quantity"],
            r["unit_price"],
            str(total)
        ))

        report["sales"]["loaded"] += 1

conn.commit()

# =====================================================
# ===================== REPORT ========================
# =====================================================
with open("data_quality_report.txt", "w") as f:
    for table, m in report.items():
        f.write(f"{table.upper()} FILE\n")
        f.write(f"Records processed: {m['processed']}\n")
        f.write(f"Duplicates removed: {m['duplicates']}\n")
        f.write(f"Rows removed due to missing PK: {m['pk_missing']}\n")
        f.write(f"Records loaded: {m['loaded']}\n\n")


cur.close()
conn.close()

print("ETL Completed Successfully")
print("Data quality report created at:", report_path) # type: ignore
