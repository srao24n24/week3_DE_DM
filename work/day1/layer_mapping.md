# Day 1, Lab 1.5: Layer Mapping

## What each layer does
- **Bronze:** raw data exactly as it came in.
- **Silver:** cleaned, validated and matched up across sources.
- **Gold:** ready for the people using it.

## Case A: Daily sales dashboard from ERP tables

| Layer | What it does |
|---|---|
| **Bronze** | Load the raw ERP extracts without changing them. Add a load timestamp and batch ID. Keep row counts so we can reconcile later. |
| **Silver** | Fix data types, remove duplicates, check required fields are filled in, standardize dates and codes, and make sure keys like product and customer IDs match. |
| **Gold** | Sales tables built for the dashboard, like daily sales by product, state and dates. |

## Case B: Clickstream plus product and order analytics

| Layer | What it does |
|---|---|
| **Bronze** | Land the raw clickstream JSON and raw product and order data as received. Only add to it, never overwrite. Add load timestamp and batch ID. |
| **Silver** | Parse the JSON into columns, remove duplicate events, standardize timestamps, filter out test or bot traffic, match customer and product keys across sources, set aside bad records, and mask personal identifiers. |
| **Gold** | Analytics tables for BI and cleaned tables for data science. |