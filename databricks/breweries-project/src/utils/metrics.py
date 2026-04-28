from pyspark.sql.functions import count, current_timestamp, lit

def write_metrics_stream(df, table_name, partition_col, checkpoint_path, target_table="one.control.event_metrics"):
    """
    Writes ingestion metrics as a streaming job.
    """

    df_metrics = df.groupBy(partition_col) \
        .agg(count("*").alias("record_count")) \
        .withColumn("table_name", lit(table_name)) \
        .withColumn("ingestion_time", current_timestamp())

    query = df_metrics.writeStream \
        .format("delta") \
        .option("checkpointLocation", f"{checkpoint_path}/metrics") \
        .outputMode("append") \
        .queryName(f"metrics_{table_name}") \
        .trigger(availableNow=True) \
        .toTable(target_table)

    return query
