# Grain and model worksheet DAY 4

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

---

<!-- - Day 4 - -->
**SCD strategy by attribute:** 
**Late arriving data strategy:** 
**Reconciliation checks:** 