# Grain and model worksheet

## Day 3
<!-- --- Lab 3.1 --- -->
**Business process:** Retail sales where customers purchase products across web, mobile, and in-store channels.
**Fact table name:** FactSales
**Grain statement beginning with One row per:** One row per order item

<!-- --- Lab 3.2 --- -->
**Dimensions:** DimDate, DimCustomer, DimProduct, DimChannel

<!-- --- Lab 3.5 --- -->
**Measures and additivity:** quantity is additive because it can be summed across dimensions to get total items sold, unit_price is non-additive because it is a per-unit rate and summing it does not have meaningful business value, and discount_pct is non-additive because it is a percentage and cannot be meaningfully summed.

<!-- --- Lab 3.6 --- -->
**Degenerate dimensions:** order_id, order_item_id

<!-- --- Lab 3.4 --- -->
**Surrogate keys:** date_key (DimDate), customer_key (DimCustomer), product_key (DimProduct), channel_key (DimChannel).

## Day 4
<!-- --- Lab 4.2 & 4.3 --- -->
**SCD strategy by attribute:** customer_name and email use Type 1 (overwrite in place, no history kept). city, state, and customer_segment use Type 2 (expire the old row, insert a new versioned row with a new customer_key).

<!-- --- Lab 4.7 --- -->
**Late arriving data strategy:** If a fact arrives before its dimension row exists, insert the dimension row right away using just the known business key, with "Unknown" placeholder values, flagged as an inferred member. When the real data shows up later, update that row in place and clear the flag, no new row needed.

**Reconciliation checks:** ?