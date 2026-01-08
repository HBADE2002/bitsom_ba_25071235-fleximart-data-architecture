# FlexiMart Data Architecture Project

**Student Name:** Abhishek Sanjay Bade
**Student ID:** bitsom_ba_25071860
**Email:** justforstorages2022@gmail.com
**Date:** 08/01/2025

## Project Overview

This project demonstrates the design and implementation of a complete data architecture for FlexiMart, covering transactional data processing, NoSQL analysis, and data warehousing. It includes building an ETL pipeline to clean and load operational data into a relational database, evaluating MongoDB for flexible product catalogs, and designing a star schema–based data warehouse to support analytical reporting and OLAP queries.

## Repository Structure
├── part1-database-etl/
│   ├── etl_pipeline.py
│   ├── schema_documentation.md
│   ├── business_queries.sql
│   └── data_quality_report.txt
├── part2-nosql/
│   ├── nosql_analysis.md
│   ├── mongodb_operations.js
│   └── products_catalog.json
├── part3-datawarehouse/
│   ├── star_schema_design.md
│   ├── warehouse_schema.sql
│   ├── warehouse_data.sql
│   └── analytics_queries.sql
└── README.md

## Technologies Used

Python 3.x, pandas, psycopg2

PostgreSQL 14 (OLTP & Data Warehouse)

MongoDB 6.0 (NoSQL product catalog)

NoSQLBooster for MongoDB

pgAdmin 4

## Setup Instructions

### Database Setup

```bash
# Create databases
createdb fleximart
createdb fleximart_dw

# Run Part 1 - ETL Pipeline
python part1-database-etl/etl_pipeline.py

# Run Part 1 - Business Queries
mysql -u root -p fleximart < part1-database-etl/business_queries.sql

# Run Part 3 - Data Warehouse
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_schema.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/warehouse_data.sql
mysql -u root -p fleximart_dw < part3-datawarehouse/analytics_queries.sql


### MongoDB Setup
mongod
use fleximart_nosql
load("part2-nosql/mongodb_operations.js")

mongosh < part2-nosql/mongodb_operations.js

## Key Learnings

Through this project, I learned how to design and implement a complete data pipeline starting from raw CSV data to analytical reporting. I gained hands-on experience with ETL processes, data quality handling, and enforcing relational integrity using PostgreSQL. The project also helped me understand when NoSQL databases like MongoDB are more suitable than relational databases. Finally, I learned how star schemas and OLAP queries enable efficient historical and multidimensional analysis.

## Challenges Faced

1. Handling data quality issues in ETL
Missing values, inconsistent formats, and duplicates required careful rule-based cleaning while preserving original primary keys.

2. Managing relational vs NoSQL differences
Understanding when to use fixed schemas (PostgreSQL) versus flexible documents (MongoDB) was critical in designing the right solution.

3. Foreign key constraints in data warehouse loading
Ensuring that all dimension keys existed before loading fact data required careful ordering and validation.

