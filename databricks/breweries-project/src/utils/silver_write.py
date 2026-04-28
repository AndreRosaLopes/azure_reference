from delta.tables import DeltaTable

def write_to_silver(df, target_table, checkpoint_path, join_cols, partition_col):
    """
    Orchestrates the WriteStream for Silver tables using MERGE logic.
    """
    
    def upsert_to_delta(microBatchDF, batchId):
        if microBatchDF.isEmpty(): return
        
        spark = microBatchDF.sparkSession
        
        if spark.catalog.tableExists(target_table):
            delta_table = DeltaTable.forName(spark, target_table)
            
            j_cols = [join_cols] if isinstance(join_cols, str) else join_cols
            merge_condition = " AND ".join([f"t.{c} = s.{c}" for c in j_cols])
            
            delta_table.alias("t").merge(
                microBatchDF.alias("s"),
                merge_condition
            ).whenNotMatchedInsertAll() \
                .execute()
        else:
            writer = microBatchDF.write.format("delta")
            if partition_col:
                writer = writer.partitionBy(partition_col)
            writer.saveAsTable(target_table)

    query = df.writeStream \
        .foreachBatch(upsert_to_delta) \
        .option("checkpointLocation", checkpoint_path) \
        .trigger(availableNow=True) \
        .start()
    
    query.awaitTermination()

def write_to_quarantine(df, table_name, target_table, checkpoint_path):
    """
    Writes invalid records to a quarantine table.
    """
    from pyspark.sql.functions import lit, current_timestamp

    query = df \
        .withColumn("error_reason", lit("json_parse_error")) \
        .withColumn("ingestion_time", current_timestamp()) \
        .writeStream \
        .format("delta") \
        .option("checkpointLocation", f"{checkpoint_path}/quarantine") \
        .outputMode("append") \
        .queryName(f"quarantine_{table_name}") \
        .trigger(availableNow=True) \
        .toTable(target_table)
    
    query.awaitTermination()
