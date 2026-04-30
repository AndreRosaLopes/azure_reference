# Databricks notebook source
# /// script
# [tool.databricks.environment]
# environment_version = "5"
# ///
# MAGIC %md
# MAGIC # Silver Pipeline - Breweries
# MAGIC Orchestration notebook for processing brewery data from Bronze to Silver.

# COMMAND ----------

# MAGIC %restart_python
# MAGIC

# COMMAND ----------

import json
from pyspark.sql.functions import col, from_json, lit, current_timestamp
from pyspark.sql.types import StructType
import os
import sys
# Adiciona o diretório pai (raiz do projeto) ao sys.path
sys.path.append(os.path.abspath('..'))

# Standard imports following best practices
from src.utils.spark_utils import add_metadata_columns, add_hash_column, apply_standard_transformations, deduplicate_data
from src.utils.data_quality import validate_not_null, filter_late_data
from src.utils.metrics import write_metrics_stream
from src.utils.silver_write import write_to_silver, write_to_quarantine

# COMMAND ----------

# Parameters
dbutils.widgets.text("table_name", "bronze_breweries")
dbutils.widgets.text("config_base_path", "/metadata/pipelines")

table_name = dbutils.widgets.get("table_name")
config_base_path = dbutils.widgets.get("config_base_path")

# COMMAND ----------


# 1. Get the directory path of the current notebook (e.g., /.../notebooks)
notebook_dir = os.getcwd()
# 2. Navigate up one level to reach the project root directory
project_root = os.path.abspath(os.path.join(notebook_dir, ".."))
# 3. Construct the dynamic paths for config and schema files
config_path = f"{project_root}/metadata/pipelines/{table_name}.json"
schema_file_path = f"{project_root}/metadata/schemas/{table_name}_schema.json"

# Load configuration
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
with open(schema_file_path, "r") as f:
    schema_dict = json.load(f)
schema = StructType.fromJson(schema_dict)

# COMMAND ----------

# 1. Read Stream from Bronze (Auto Loader)
df_raw = spark.readStream.format("cloudFiles") \
    .option("cloudFiles.format", "json") \
    .option("cloudFiles.schemaLocation", schema_path) \
    .option("optimizeWrite", "true")
    .load(source_path)

# COMMAND ----------

# 2. Parse and Split Quality
# In this case, we assume the source is the raw JSON from the API volume
#df_parsed = df_raw # Auto Loader already parsed top level if configured, but let's be explicit if needed
# For this example, let's assume Auto Loader handles the JSON structure via schema

# 3. Apply Modular Transformations
df_silver = add_metadata_columns(df_raw)
df_silver = add_hash_column(df_silver)
df_silver = apply_standard_transformations(df_silver, partition_col)
df_silver = validate_not_null(df_silver, join_cols)
df_silver = deduplicate_data(df_silver, join_cols[0])



# COMMAND ----------

display(config)

# COMMAND ----------

display(schema_dict)

# COMMAND ----------

display(df_raw, checkpointLocation = "/Volumes/one/silver/schemas/temp_display_checkpoint")

# COMMAND ----------

# MAGIC %sql
# MAGIC create schema if not exists one.silver
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS one.silver.schemas;

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists one.silver.breweries

# COMMAND ----------

# MAGIC %sql
# MAGIC create table if not exists one.silver.quarantine_breweries

# COMMAND ----------

# MAGIC %sql
# MAGIC Create volume if not exists one.silver.checkpoints

# COMMAND ----------

print("Estrutura do DataFrame:")
df_silver.printSchema()


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE one.silver.breweries (
# MAGIC   address_1 STRING,
# MAGIC   address_2 STRING,
# MAGIC   address_3 STRING,
# MAGIC   brewery_type STRING,
# MAGIC   city STRING,
# MAGIC   country STRING,
# MAGIC   id STRING,
# MAGIC   latitude STRING,
# MAGIC   longitude STRING,
# MAGIC   name STRING,
# MAGIC   phone STRING,
# MAGIC   postal_code STRING,
# MAGIC   state STRING,
# MAGIC   state_province STRING,
# MAGIC   street STRING,
# MAGIC   website_url STRING,
# MAGIC   _rescued_data STRING,
# MAGIC   ingestion_time TIMESTAMP NOT NULL,
# MAGIC   source_file STRING NOT NULL,
# MAGIC   row_hash STRING NOT NULL
# MAGIC )
# MAGIC USING DELTA;

# COMMAND ----------

print("\nColunas disponíveis:")
print(df_silver.columns)

# COMMAND ----------

# 4. Write to Silver
write_to_silver(
    df_silver, 
    target_table, 
    join_cols, 
    partition_col,
    checkpoint_path
)

# COMMAND ----------

display(one.silver.breweries)

# COMMAND ----------

df_raw.count()

# COMMAND ----------

# MAGIC %sql
# MAGIC select count(*) from one.silver.breweries

# COMMAND ----------

df_raw2 = spark.read \
    .format("json") \
    .load(source_path)

# COMMAND ----------

df_raw2.count()
