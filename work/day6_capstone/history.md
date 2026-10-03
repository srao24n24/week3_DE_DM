# Day 6: Retail Analytics Platform History Strategy

**SCD strategy by attribute:**
- customer_name, email: Type 1 (overwrite in place, no history kept). These are corrections, not meaningful business changes worth tracking.
- city, state, customer_segment: Type 2 (expire the old row, insert a new versioned row with a new customer_key). These represent real changes in the customer's situation that affect how past sales should be analyzed, so history must be preserved.

**Effective-date lookup (used when loading FactSales/FactPayments):**
```sql
SELECT dc.customer_key FROM DimCustomer dc
WHERE dc.customer_id = @order_customer_id AND @order_date >= dc.effective_from AND @order_date < dc.effective_to;
```
