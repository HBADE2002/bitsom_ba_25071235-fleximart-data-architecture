
---

# NoSQL Database Analysis – FlexiMart

## Task 2.1: NoSQL Justification Report

---

## Section A: Limitations of RDBMS 

Relational databases like MySQL or PostgreSQL enforce a fixed schema, which becomes restrictive when dealing with highly diverse product data. In FlexiMart’s case, different products have different attributes—for example, laptops require fields such as RAM, processor, and storage, while shoes require size, color, and material. In an RDBMS, accommodating these differences would require adding many nullable columns or creating multiple related tables, making the schema complex and inefficient.

Frequent introduction of new product types would also force repeated schema changes using `ALTER TABLE`, which can be time-consuming and risky in production environments. Additionally, storing customer reviews as nested data is not natural in a relational model. Reviews would need a separate table and joins to retrieve them, increasing query complexity and reducing performance. Overall, the rigid structure and normalization requirements of RDBMS make it less suitable for rapidly evolving, heterogeneous product catalogs.

---

## Section B: NoSQL Benefits 

MongoDB addresses these challenges through its flexible, document-based data model. Each product can be stored as a JSON-like document with attributes specific to that product type. For example, a laptop document can include RAM and processor fields, while a shoe document can include size and color, without affecting other documents. This flexible schema eliminates the need for frequent schema migrations when new product categories are introduced.

MongoDB also supports embedded documents, allowing customer reviews to be stored directly inside the product document. This makes data retrieval simpler and faster, as product details and reviews can be fetched in a single query without joins. Furthermore, MongoDB is designed for horizontal scalability through sharding, enabling FlexiMart to efficiently handle a growing product catalog and increasing traffic by distributing data across multiple servers. These features make MongoDB well-suited for dynamic and scalable e-commerce applications.

---

## Section C: Trade-offs 

Despite its advantages, MongoDB has certain drawbacks compared to relational databases. First, it does not enforce strong schema-level constraints by default, which can lead to inconsistent data if validation rules are not carefully implemented at the application level. Second, MongoDB is less suitable for complex transactional operations involving multiple documents, as multi-document ACID transactions are more limited and can impact performance. For use cases requiring strict consistency, complex joins, and strong relational integrity, a traditional RDBMS like MySQL may still be a better choice.

---


