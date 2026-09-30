-- Day 3, Lab 3.7: DDL

-- DDL for DimDate
CREATE TABLE DimDate (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT,
    quarter INT,
    month INT,
    month_name VARCHAR(20),
    day INT
);

-- DDL for DimCustomer
CREATE TABLE DimCustomer (
    customer_key INT IDENTITY PRIMARY KEY,
    customer_id INT NOT NULL,
    customer_name VARCHAR(100),
    email VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    customer_segment VARCHAR(50),
    signup_date DATE
);

-- DDL for DimProduct
CREATE TABLE DimProduct (
    product_key INT IDENTITY PRIMARY KEY,
    product_id INT NOT NULL,
    product_name VARCHAR(100),
    brand VARCHAR(100),
    cost_price DECIMAL(10,2),
    list_price DECIMAL(10,2),
    category_id INT,
    category_name VARCHAR(100)
);

-- DDL for DimChannel
CREATE TABLE DimChannel (
    channel_key INT IDENTITY PRIMARY KEY,
    sales_channel VARCHAR(20) NOT NULL
);

-- DDL for FactSales
CREATE TABLE FactSales (
    order_item_id INT NOT NULL,
    order_id INT NOT NULL,
    date_key INT REFERENCES DimDate(date_key),
    customer_key INT REFERENCES DimCustomer(customer_key),
    product_key INT REFERENCES DimProduct(product_key),
    channel_key INT REFERENCES DimChannel(channel_key),
    quantity INT,
    unit_price DECIMAL(10,2),
    discount_pct DECIMAL(5,2)
);

-- DDL for FactPayments
CREATE TABLE FactPayments (
    payment_id INT NOT NULL,
    order_id INT NOT NULL,
    date_key INT REFERENCES DimDate(date_key),
    payment_method VARCHAR(30),
    payment_status VARCHAR(20)
);

