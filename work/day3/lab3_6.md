# Day 3, Lab 3.6: Design rationale

**Is order_id a degenerate dimension?**

Yes because order_id sits in FactSales to say which order a line item came from, it has no attributes of its own like a name or a date, and there's no separate table for it. Everything about it already comes from the other dimensions, so order_id doesn't need a table.

**Does payment need its own fact table?**

Yes, Payments has 480 rows for 600 orders, so it's not one row per order and not one row per order item, it has its own grain. Since FactSales grain is fixed at one row per order item, payment measures can't be put in without mixing two different grains in one table. So payment becomes a second fact table called, FactPayments, and is kept separate.