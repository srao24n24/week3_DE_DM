# Day 3, Lab 3.4: Key mapping
 
| Table | Business key | Surrogate key | Relationship |
|---|---|---|---|
| DimDate | full_date | date_key | FactSales.date_key --> DimDate.date_key |
| DimCustomer | customer_id | customer_key | FactSales.customer_key --> DimCustomer.customer_key |
| DimProduct | product_id | product_key | FactSales.product_key --> DimProduct.product_key |
| DimChannel | sales_channel | channel_key | FactSales.channel_key --> DimChannel.channel_key |
 