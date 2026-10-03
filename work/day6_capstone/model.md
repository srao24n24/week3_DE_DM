# Day 6: Retail Analytics Platform Grain and Model

**Business process:** Retail sales where customers purchase products across web, mobile, and in-store channels.

**Fact table name:** FactSales, FactPayments

**Grain statement beginning with One row per:** One row per order item for FactSales, One row per payment attempt for FactPayments.

**Dimensions:** DimDate, DimCustomer, DimProduct, DimChannel

**Measures and additivity:**
- FactSales: quantity is additive because it can be summed across dimensions to get total items sold, unit_price is non-additive because it is a per-unit rate and summing it does not have meaningful business value, and discount_pct is non-additive because it is a percentage and cannot be meaningfully summed.
- FactPayments: no numeric measures, payments file has no amount column, only payment_date, payment_method, and payment_status. It's a factless fact table, used for counting events.

**Degenerate dimensions:** order_id, order_item_id (FactSales) and payment_id, order_id (FactPayments)

**Surrogate keys:** date_key (DimDate), customer_key (DimCustomer), product_key (DimProduct), channel_key (DimChannel).

**SCD strategy by attribute:** customer_name and email use Type 1 (overwrite in place, no history kept). city, state, and customer_segment use Type 2 (expire the old row, insert a new versioned row with a new customer_key).

**Late arriving data strategy:** If a fact arrives before its dimension row exists, insert the dimension row right away using just the known business key, with "Unknown" placeholder values, flagged as an inferred member. When the real data shows up later, update that row in place and clear the flag, no new row needed.

**Reconciliation checks:**  Row counts, key uniqueness, referential integrity, reject handling, and financial totals reconciliation (See controls.md for in-depth).