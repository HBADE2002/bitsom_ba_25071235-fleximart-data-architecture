# Part 1: Relational Database & ETL Pipeline

## Overview
This part focuses on building an ETL pipeline to clean and load raw transactional data into a relational database. The pipeline processes customer, product, and sales data containing data quality issues such as missing values, duplicates, and inconsistent formats.

## Objectives
- Read raw CSV files containing customer, product, and sales data
- Clean and standardize data (dates, phone numbers, categories)
- Remove duplicate records and handle missing values
- Load cleaned data into a PostgreSQL database
- Generate a data quality report summarizing the ETL process

## Files Included
- `etl_pipeline.py` – Python ETL script for data extraction, transformation, and loading
- `schema_documentation.md` – Documentation of the relational database schema
- `business_queries.sql` – SQL queries answering business questions
- `data_quality_report.txt` – Summary of data processing and quality metrics
- `requirements.txt` – Python dependencies required to run the ETL pipeline

## How to Run
1. Ensure PostgreSQL is running and the `fleximart` database exists.
2. Place raw CSV files inside the `data/` directory.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
