# Databricks notebook source
# MAGIC %md
# MAGIC # Silver Pipeline - Breweries
# MAGIC Orchestration notebook for processing brewery data from Bronze to Silver.

# COMMAND ----------

import json
from pyspark.sql.functions import col, from_json, lit, current_timestamp
from pyspark.sql.types import StructType

# Standard imports following best practices
from src.utils.spark_utils import add_metadata_columns, add_hash_column, apply_standard_transformations, deduplicate_data
from src.utils.data_quality import validate_not_null, filter_late_data
from src.utils.metrics import write_metrics_stream
from src.tables.table_manager import write_to_silver, write_to_quarantine

# COMMAND ----------

# Parameters
dbutils.widgets.text("table_name", "bronze_breweries")
dbutils.widgets.text("config_base_path", "/data_engineer/metadata/pipelines")

table_name = dbutils.widgets.get("table_name")
config_base_path = dbutils.widgets.get("config_base_path")

# COMMAND ----------

# Load configuration
config_path = f"/Workspace{config_base_path}/{table_name}.json"
with open(config_path, "r") as f:
    config = json.load(f)

# Extracted variables
source_path      = config["source_path"]
target_table     = config["target_table"]
quarantine_table = config.get("quarantine_table")
checkpoint_path  = config["checkpoint_path"]
schema_path      = config["schema_path"]
watermark_days   = config["watermark_days"]
join_cols        = config["join_cols"]
partition_col    = config["partition_column"]

# Load schema
schema_file_path = f"/Workspace{config_base_path}/schemas/{table_name}_schema.json"
with open(schema_file_path, "r") as f:
    schema_dict = json.load(f)
schema = StructType.fromJson(schema_dict)

# COMMAND ----------

# 1. Read Stream from Bronze (Auto Loader)
df_raw = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", schema_path) \
    .load(source_path)

# COMMAND ----------

# 2. Parse and Split Quality
# In this case, we assume the source is the raw JSON from the API volume
df_parsed = df_raw # Auto Loader already parsed top level if configured, but let's be explicit if needed
# For this example, let's assume Auto Loader handles the JSON structure via schema

# 3. Apply Modular Transformations
df_silver = add_metadata_columns(df_raw)
df_silver = add_hash_column(df_silver)
df_silver = apply_standard_transformations(df_silver, partition_col)
df_silver = validate_not_null(df_silver, join_cols)
df_silver = deduplicate_data(df_silver, join_cols[0])

# 4. Write to Silver
write_to_silver(
    df_silver, 
    target_table, 
    checkpoint_path, 
    join_cols, 
    partition_col
)

# 5. Write metrics
write_metrics_stream(
    df_silver,
    table_name,
    partition_col,
    checkpoint_path
)

# 6. Save Quarantine (placeholder for invalid data logic)
# In a real scenario, we'd have a specific df_invalid from a parsing step
# write_to_quarantine(df_invalid, table_name, quarantine_table, checkpoint_path)
