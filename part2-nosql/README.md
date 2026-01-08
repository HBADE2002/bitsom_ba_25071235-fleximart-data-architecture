# Part 2: NoSQL Database Analysis (MongoDB)

## Overview
This part evaluates MongoDB as a NoSQL solution for handling a flexible and diverse product catalog. It demonstrates MongoDB’s ability to manage semi-structured data and nested documents such as product specifications and customer reviews.

## Objectives
- Analyze limitations of relational databases for heterogeneous product data
- Justify the use of MongoDB for flexible schemas
- Perform CRUD and aggregation operations using MongoDB

## Files Included
- `nosql_analysis.md` – Theoretical justification for using MongoDB
- `mongodb_operations.js` – MongoDB scripts for data loading and querying
- `products_catalog.json` – Sample product catalog data with nested attributes

## How to Run
1. Start MongoDB server (`mongod`).
2. Open NoSQLBooster for MongoDB and connect to `mongodb://localhost:27017`.
3. Switch to database:
   ```js
   use fleximart_nosql