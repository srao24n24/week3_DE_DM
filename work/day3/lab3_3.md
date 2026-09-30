# Day 3, Lab 3.3: Star Schema Diagram

## Dimension and Facts Table 
DimDate
| date_key | full_date | year | quarter | month | month_name | day |

DimCustomer
| customer_key | customer_id | customer_name | email | city | state | customer_segment | signup_date |

DimProduct
| product_key | product_id | product_name | brand | cost_price | list_price | category_id | category_name |

DimChannel
| channel_key | sales_channel |

FactSales
| order_item_id (degenerate) | order_id (degenerate) | date_key (FK) | customer_key (FK) | product_key (FK) | channel_key (FK) | quantity | unit_price | discount_pct |

