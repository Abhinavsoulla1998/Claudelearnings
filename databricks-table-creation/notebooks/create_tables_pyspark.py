# Databricks notebook source
# MAGIC %md
# MAGIC # Create Delta tables with PySpark
# MAGIC Shows three ways to create a table: explicit schema, from a DataFrame, and with the DeltaTable builder.

# COMMAND ----------

from pyspark.sql import functions as F
from pyspark.sql.types import (StructType, StructField, LongType, StringType,
                               DecimalType, DateType, TimestampType)
from delta.tables import DeltaTable

CATALOG = "main"
SCHEMA = "sales"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOG}.{SCHEMA}")

# COMMAND ----------
# 1) Create an empty table from an explicit schema

orders_schema = StructType([
    StructField("order_id", LongType(), False),
    StructField("customer_id", LongType(), False),
    StructField("order_date", DateType(), False),
    StructField("status", StringType(), False),
    StructField("amount", DecimalType(12, 2), False),
])

(spark.createDataFrame([], orders_schema)
    .write.format("delta")
    .mode("ignore")                       # do nothing if the table already exists
    .partitionBy("order_date")
    .saveAsTable(f"{CATALOG}.{SCHEMA}.orders_py"))

# COMMAND ----------
# 2) Create a table from a DataFrame

customers = spark.createDataFrame(
    [(1, "Ada", "Lovelace", "ada@example.com", "UK"),
     (2, "Grace", "Hopper", "grace@example.com", "US")],
    "customer_id long, first_name string, last_name string, email string, country string",
).withColumn("created_at", F.current_timestamp())

(customers.write.format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{CATALOG}.{SCHEMA}.customers_py"))

# COMMAND ----------
# 3) Create a table with the DeltaTable builder (supports comments, properties, generated columns)

(DeltaTable.createIfNotExists(spark)
    .tableName(f"{CATALOG}.{SCHEMA}.events")
    .addColumn("event_id", "BIGINT", nullable=False)
    .addColumn("event_ts", "TIMESTAMP")
    .addColumn("event_date", "DATE", generatedAlwaysAs="CAST(event_ts AS DATE)")
    .addColumn("payload", "STRING")
    .partitionedBy("event_date")
    .comment("Raw events")
    .property("delta.enableChangeDataFeed", "true")
    .execute())

# COMMAND ----------
# Verify

display(spark.sql(f"SHOW TABLES IN {CATALOG}.{SCHEMA}"))
display(spark.sql(f"DESCRIBE EXTENDED {CATALOG}.{SCHEMA}.events"))
