from pyspark.sql.functions import current_timestamp, input_file_name, to_date, col, md5, concat_ws

def add_metadata_columns(df):
    """Adds audit columns to the DataFrame."""
    return df \
        .withColumn("ingestion_time", current_timestamp()) \
        .withColumn("source_file",  col("_metadata.file_path"))

def add_hash_column(df, column_name="row_hash"):
    """Calculates MD5 hash of all columns to track changes."""
    # We exclude metadata columns from hash to ensure business data changes are caught
    exclude_cols = ["_metadata","ingestion_time", "source_file", "year", "month", "day"]
    business_cols = [c for c in df.columns if c not in exclude_cols]
    return df.withColumn(column_name, md5(concat_ws("||", *business_cols)))

def apply_standard_transformations(df, partition_col, event_ts_col=None):
    """Casts dates and prepares the partition column."""
    return df

def deduplicate_data(df, merge_key, order_col=None):
    """Generic deduplication logic."""
    if order_col:
        return df.dropDuplicates([merge_key, order_col])
    return df.dropDuplicates([merge_key])
