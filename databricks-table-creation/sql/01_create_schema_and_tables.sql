-- Databricks SQL: create a schema and Delta tables (Unity Catalog)
-- Replace `main` with your catalog name if needed.

CREATE SCHEMA IF NOT EXISTS main.sales
COMMENT 'Sales demo schema';

-- Managed Delta table with constraints, partitioning and table properties
CREATE TABLE IF NOT EXISTS main.sales.customers (
  customer_id   BIGINT GENERATED ALWAYS AS IDENTITY,
  first_name    STRING   NOT NULL,
  last_name     STRING   NOT NULL,
  email         STRING,
  country       STRING,
  created_at    TIMESTAMP DEFAULT current_timestamp(),
  CONSTRAINT customers_pk PRIMARY KEY (customer_id)
)
USING DELTA
COMMENT 'One row per customer'
TBLPROPERTIES (
  'delta.autoOptimize.optimizeWrite' = 'true',
  'delta.autoOptimize.autoCompact'   = 'true',
  'delta.enableChangeDataFeed'       = 'true'
);

CREATE TABLE IF NOT EXISTS main.sales.orders (
  order_id      BIGINT GENERATED ALWAYS AS IDENTITY,
  customer_id   BIGINT        NOT NULL,
  order_date    DATE          NOT NULL,
  status        STRING        NOT NULL,
  amount        DECIMAL(12,2) NOT NULL,
  CONSTRAINT orders_pk PRIMARY KEY (order_id),
  CONSTRAINT orders_customer_fk FOREIGN KEY (customer_id) REFERENCES main.sales.customers (customer_id),
  CONSTRAINT orders_amount_positive CHECK (amount >= 0)
)
USING DELTA
PARTITIONED BY (order_date)
COMMENT 'One row per order';

-- Create a table from a query (CTAS)
CREATE OR REPLACE TABLE main.sales.daily_revenue AS
SELECT order_date, SUM(amount) AS revenue, COUNT(*) AS orders
FROM main.sales.orders
GROUP BY order_date;

-- External table pointing at cloud storage (adjust the location)
-- CREATE TABLE IF NOT EXISTS main.sales.raw_events
-- USING DELTA
-- LOCATION 's3://my-bucket/raw/events';

-- Table from files (CSV) using read_files
-- CREATE TABLE main.sales.customers_csv AS
-- SELECT * FROM read_files('/Volumes/main/sales/landing/customers.csv', format => 'csv', header => true);
