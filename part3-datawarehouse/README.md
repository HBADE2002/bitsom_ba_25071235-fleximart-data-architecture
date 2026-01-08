# Part 3: Data Warehouse & OLAP Analytics

## Overview
This part focuses on designing and implementing a data warehouse using a star schema. The warehouse supports historical sales analysis and enables efficient OLAP queries for business intelligence.

## Objectives
- Design a star schema with fact and dimension tables
- Populate dimension and fact tables with realistic sample data
- Perform OLAP queries such as drill-down, ranking, and segmentation

## Files Included
- `star_schema_design.md` – Documentation of the star schema design and design decisions
- `warehouse_schema.sql` – SQL script to create warehouse tables
- `warehouse_data.sql` – Sample data inserts for dimensions and fact table
- `analytics_queries.sql` – OLAP queries for analytical scenarios

## Warehouse Design
- **Fact Table:** `fact_sales` (sales transactions)
- **Dimensions:** `dim_date`, `dim_product`, `dim_customer`

## How to Run
1. Ensure PostgreSQL is running and the `fleximart_dw` database exists.
2. Create warehouse schema:
   ```bash
   psql -d fleximart_dw -f warehouse_schema.sql