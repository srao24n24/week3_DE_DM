# Day 6: Retail Analytics Platform Architecture Decision

**Business objective:** Give BI, finance, and data science teams reliable, governed analytics on customer behavior, product performance, and sales across the full retail dataset, by integrating customer, product, order, order-item, and payment data into one platform.

**Sources and formats:** customers, products, categories, orders, order_items (line-item grain) and payments, all structured.

**Required latency:** Daily.

**Consumers:** BI analysts and finance, and data engineers/future lakehouse implementers who need raw history preserved.

**Recommended store:** Warehouse

**Processing:** Batch

**Pattern:** ETL

**Proposed Bronze Silver Gold responsibilities:**
- Bronze: raw customers, products, categories, orders, order_items and payments data, exactly as received. Nothing is dropped.
- Silver: validate and clean data, remove duplicates, standardize data types and dates, apply SCD Type 1/2 rules to customer and product dimensions, match keys across tables, set aside bad records.
- Gold: the sales star schema, FactSales, FactPayments, and the DimDate, DimCustomer,DimProduct and DimChannel dimensions, ready for BI and finance reporting.

**Security governance and quality considerations:** Role-based access by layer. Row-count and key reconciliation between layers. Retention and lineage expectations should match whatever the business specifies, not assumed.

**Decision rationale and rejected alternative:**
- Rationale: All six sources are fully structured, and the end goal is a governed star schema for BI and finance, exactly what a Warehouse is built for (T-SQL, multi-table transactions, dimensional modeling). ETL fits because payments and financial order data need validation and reconciliation before they reach the reporting layer, auditors and finance should only see trusted data.
- Rejected alternative: Lakehouse only. A lakehouse is strongest when it needs to handle semi-structured or unstructured data and heavy Spark-based data science, neither applies here, every source is a clean relational table and the deliverable is a reporting-ready star schema.