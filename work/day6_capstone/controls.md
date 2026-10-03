# Day 6: Retail Analytics Platform Controls

**Counts:** After every load, compare the row count of the target table against the expected count which is source rows in - duplicates, +/- inserts and updates. If the count doesn't match, the load is flagged as failed and the watermark is not advanced.

**Keys:** Every dimension's surrogate key (customer_key, product_key, channel_key, date_key) must be unique, checked after each load. Every fact table's degenerate dimensions (order_id, order_item_id, payment_id) should have no unexpected duplicates after deduplication.

**Referential integrity:** Every foreign key on FactSales and FactPayments must match an existing surrogate key in its dimension table, no orphaned customer_key, product_key, channel_key, or date_key. Since a Warehouse doesn't enforce foreign keys automatically, this needs an explicit check during the ETL load, any fact row that fails the check is handled  rather than silently loaded with a broken key.

**Reject handling:** Rows that fail validation such as, bad data types, missing required fields, a lookup that returns no match are written to a separate reject table instead of being dropped silently or crashing the load. Each rejected row is logged with the reason it failed, so it can be reviewed and reprocessed once the source data is fixed.

**Financial totals:** Sum of quantity × unit_price × (1 - discount_pct/100) across FactSales for a given period should reconcile against the source order_items totals for that same period, confirming no rows were lost or double-counted during the load. Payment totals (count of successful vs failed payments) should similarly reconcile against payments.csv counts for the same period.