
---

# Entity–Relationship Description 

---

## ENTITY: customers

**Purpose:**
Stores master information about customers registered on the FlexiMart platform.

**Attributes:**

* **customer_id**: Unique identifier for each customer (Primary Key, auto-incremented)
* **first_name**: Customer’s first name
* **last_name**: Customer’s last name
* **email**: Customer’s email address (must be unique)
* **phone**: Customer’s contact number
* **city**: City where the customer resides
* **registration_date**: Date when the customer registered on the platform

**Relationships:**

* One customer can place **many orders**
* Relationship type: **1 : M** with the `orders` table

---

## ENTITY: products

**Purpose:**
Stores information about products available for sale on FlexiMart.

**Attributes:**

* **product_id**: Unique identifier for each product (Primary Key, auto-incremented)
* **product_name**: Name of the product
* **category**: Product category (e.g., Electronics, Fashion, Groceries)
* **price**: Price of a single unit of the product
* **stock_quantity**: Number of units currently available in inventory

**Relationships:**

* One product can appear in **many order items**
* Relationship type: **1 : M** with the `order_items` table

---

## ENTITY: orders

**Purpose:**
Stores high-level information about customer orders.

**Attributes:**

* **order_id**: Unique identifier for each order (Primary Key, auto-incremented)
* **customer_id**: Identifier of the customer who placed the order (Foreign Key)
* **order_date**: Date when the order was placed
* **total_amount**: Total monetary value of the order
* **status**: Current status of the order (e.g., Pending, Completed, Cancelled)

**Relationships:**

* Each order is placed by **one customer**
* One order can contain **many order items**
* Relationships:

  * **M : 1** with `customers`
  * **1 : M** with `order_items`

---

## ENTITY: order_items

**Purpose:**
Stores detailed line-item information for each order.

**Attributes:**

* **order_item_id**: Unique identifier for each order item (Primary Key, auto-incremented)
* **order_id**: Identifier of the associated order (Foreign Key)
* **product_id**: Identifier of the associated product (Foreign Key)
* **quantity**: Number of units of the product ordered
* **unit_price**: Price per unit at the time of purchase
* **subtotal**: Calculated value (quantity × unit_price)

**Relationships:**

* Each order item belongs to **one order**
* Each order item refers to **one product**

---

# Normalization Explanation (3NF)

The FlexiMart database schema is designed in **Third Normal Form (3NF)** to ensure data integrity and eliminate redundancy.

### Functional Dependencies:

* `customer_id → first_name, last_name, email, phone, city, registration_date`
* `product_id → product_name, category, price, stock_quantity`
* `order_id → customer_id, order_date, total_amount, status`
* `order_item_id → order_id, product_id, quantity, unit_price, subtotal`

Each table has a **single-column primary key**, and all non-key attributes are **fully functionally dependent** on that primary key. There are no partial dependencies, since no table uses a composite primary key.

The design also avoids **transitive dependencies**. For example, customer details are stored only in the `customers` table and are referenced via foreign keys in the `orders` table, rather than being duplicated. Similarly, product details are stored only once in the `products` table and referenced through `order_items`.

### Anomaly Prevention:

* **Update anomaly** is avoided because customer and product details are stored in exactly one place.
* **Insert anomaly** is prevented because new customers or products can be added independently without requiring an order.
* **Delete anomaly** is avoided because deleting an order does not remove customer or product records.

Thus, the schema satisfies all conditions of **3NF**, making it efficient, consistent, and scalable.

---

# Sample Data Representation

### customers

| customer_id | first_name | last_name | email                                                   | city      |
| ----------- | ---------- | --------- | ------------------------------------------------------- | --------- |
| 1           | Rahul      | Sharma    | [rahul.sharma@gmail.com](mailto:rahul.sharma@gmail.com) | Bangalore |
| 2           | Priya      | Patel     | [priya.patel@yahoo.com](mailto:priya.patel@yahoo.com)   | Mumbai    |

---

### products

| product_id | product_name       | category    | price    | stock_quantity |
| ---------- | ------------------ | ----------- | -------- | -------------- |
| 1          | Samsung Galaxy S21 | Electronics | 45999.00 | 150            |
| 2          | Nike Running Shoes | Fashion     | 3499.00  | 80             |

---

### orders

| order_id | customer_id | order_date | total_amount | status    |
| -------- | ----------- | ---------- | ------------ | --------- |
| 1        | 1           | 2024-01-15 | 45999.00     | Completed |
| 2        | 2           | 2024-01-16 | 5998.00      | Completed |

---

### order_items

| order_item_id | order_id | product_id | quantity | unit_price | subtotal |
| ------------- | -------- | ---------- | -------- | ---------- | -------- |
| 1             | 1        | 1          | 1        | 45999.00   | 45999.00 |
| 2             | 2        | 2          | 2        | 2999.00    | 5998.00  |


