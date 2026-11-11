-- SQLite starter table. The processed CSV contains these fields plus revenue,
-- cost, profit, and profit_margin. Adapt this schema to your actual source.
CREATE TABLE sales (
    order_id TEXT NOT NULL,
    order_date TEXT NOT NULL,
    customer_id TEXT,
    customer_name TEXT,
    region TEXT,
    product_id TEXT,
    product_name TEXT,
    category TEXT,
    quantity REAL NOT NULL,
    unit_price REAL NOT NULL,
    unit_cost REAL NOT NULL
);
