
---

# Star Schema Design – FlexiMart Data Warehouse


---

### FACT TABLE: `fact_sales`

**Grain:**
One row per **product per order line item**. Each record represents the sale of a specific product to a specific customer on a specific date.

**Business Process:**
Sales transactions generated from customer purchases.

**Measures (Numeric Facts):**

* **quantity_sold:** Number of units sold in the transaction
* **unit_price:** Price per unit at the time of sale
* **discount_amount:** Discount applied to the transaction
* **total_amount:** Final transaction amount
  *(calculated as quantity_sold × unit_price − discount_amount)*

**Foreign Keys:**

* **date_key → dim_date**
* **product_key → dim_product**
* **customer_key → dim_customer**

These foreign keys connect the fact table to its descriptive dimensions, enabling multi-dimensional analysis.

---

### DIMENSION TABLE: `dim_date`

**Purpose:**
Provides a comprehensive date dimension for time-based analysis such as daily, monthly, quarterly, and yearly trends.

**Type:**
Conformed dimension (shared consistently across all fact tables).

**Attributes:**

* **date_key (PK):** Surrogate key in YYYYMMDD format
* **full_date:** Actual calendar date
* **day_of_week:** Name of the day (Monday, Tuesday, etc.)
* **day_of_month:** Day number within the month
* **month:** Numeric month (1–12)
* **month_name:** Month name (January, February, etc.)
* **quarter:** Quarter of the year (Q1–Q4)
* **year:** Calendar year
* **is_weekend:** Boolean flag indicating weekend or weekday

---

### DIMENSION TABLE: `dim_product`

**Purpose:**
Stores descriptive information about products to enable product-level and category-level analysis.

**Attributes:**

* **product_key (PK):** Surrogate key (auto-incremented)
* **product_id:** Business identifier from the source system
* **product_name:** Name of the product
* **category:** High-level product category (e.g., Electronics, Fashion)
* **subcategory:** More granular product classification
* **unit_price:** Standard unit price of the product

This dimension supports analysis such as sales by category, subcategory, and pricing trends.

---

### DIMENSION TABLE: `dim_customer`

**Purpose:**
Stores descriptive customer information for customer-centric analysis.

**Attributes:**

* **customer_key (PK):** Surrogate key (auto-incremented)
* **customer_id:** Business identifier from the source system
* **customer_name:** Full name of the customer
* **city:** City of residence
* **state:** State or region
* **customer_segment:** Customer classification (e.g., Retail, Corporate, Premium)

This dimension enables segmentation analysis, geographic analysis, and customer behavior insights.

---

## Section 2: Design Decisions

The chosen granularity for the fact table is **transaction line-item level**, meaning one row per product per order. This level of detail provides maximum analytical flexibility, allowing the business to analyze sales by individual products, customers, dates, and categories. Higher-level grains (such as one row per order) would lose important information about product-level performance and prevent accurate aggregation of quantities and revenue.

Surrogate keys are used instead of natural keys to ensure consistency, performance, and historical tracking. Natural keys such as product_id or customer_id can change over time due to business system updates, whereas surrogate keys remain stable. Using integer surrogate keys also improves join performance in large fact tables.

This star schema design supports **drill-down** and **roll-up** operations efficiently. Analysts can roll up data from daily to monthly or yearly levels using the date dimension, or drill down from category-level sales to individual products or customers. The clear separation of facts and dimensions enables fast and intuitive analytical queries.

---

## Section 3: Sample Data Flow

### Source Transaction (OLTP System)

* **Order ID:** 101
* **Customer:** John Doe
* **Product:** Laptop
* **Quantity:** 2
* **Unit Price:** ₹50,000
* **Order Date:** 2024-01-15

---

### Data Warehouse Representation

#### `fact_sales`

```json
{
  "date_key": 20240115,
  "product_key": 5,
  "customer_key": 12,
  "quantity_sold": 2,
  "unit_price": 50000,
  "discount_amount": 0,
  "total_amount": 100000
}
```

#### `dim_date`

```json
{
  "date_key": 20240115,
  "full_date": "2024-01-15",
  "day_of_week": "Monday",
  "month": 1,
  "month_name": "January",
  "quarter": "Q1",
  "year": 2024,
  "is_weekend": false
}
```

#### `dim_product`

```json
{
  "product_key": 5,
  "product_id": "P007",
  "product_name": "Laptop",
  "category": "Electronics",
  "subcategory": "Computers",
  "unit_price": 50000
}
```

#### `dim_customer`

```json
{
  "customer_key": 12,
  "customer_id": "C021",
  "customer_name": "John Doe",
  "city": "Mumbai",
  "state": "Maharashtra",
  "customer_segment": "Retail"
}
```




