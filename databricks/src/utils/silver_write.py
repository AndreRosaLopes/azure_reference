def write_to_silver_batch(df, target_table, join_cols, partition_col):
    """
    Writes a DataFrame to a Silver table using MERGE logic (Batch version).
    Ensures idempotency and uses Partition Pruning for performance.
    """
    spark = df.sparkSession
    
    # Registra o DataFrame como uma view temporária para o SQL
    df.createOrReplaceTempView("batch_updates")
    
    # 2. Constrói a condição de JOIN pelo ID

    j_cols = [join_cols] if isinstance(join_cols, str) else join_cols
    merge_condition = " AND ".join([f"t.{c} = s.{c}" for c in j_cols ])
    
    # 3. Executa o MERGE (Insert-Only para deduplicação)
    spark.sql(f"""
        MERGE INTO {target_table} t
        USING batch_updates s
        ON {merge_condition}
        WHEN NOT MATCHED THEN INSERT *
    """)
    
    # Limpeza da view
    spark.catalog.dropTempView("batch_updates")


def write_to_silver(df, target_table, join_cols, partition_col, checkpoint_location):
    """
    Writes a streaming DataFrame to a Silver table using MERGE logic via foreachBatch.
    Includes the .trigger(availableNow=True) for compatibility with Serverless compute.
    """
    
    def upsert_to_delta(micro_batch_df, batch_id):
        """
        Processes each micro-batch as a standard batch DataFrame.
        """
        # Register the micro-batch DataFrame as a temporary view
        view_name = "batch_updates"
        micro_batch_df.createOrReplaceTempView(view_name)
        
        # Construct the JOIN condition dynamically
        j_cols = [join_cols] if isinstance(join_cols, str) else join_cols
        merge_condition = " AND ".join([f"t.{c} = s.{c}" for c in j_cols])
        
        # Execute the MERGE statement (Insert-Only)
        micro_batch_df.sparkSession.sql(f"""
            MERGE INTO {target_table} t
            USING {view_name} s
            ON {merge_condition}
            WHEN NOT MATCHED THEN INSERT *
        """)
        
        # Remove the temporary view
        micro_batch_df.sparkSession.catalog.dropTempView(view_name)

    # Start the write stream with AvailableNow trigger
    return (df.writeStream
            .foreachBatch(upsert_to_delta)
            .outputMode("update")
            .option("checkpointLocation", checkpoint_location)
            .trigger(availableNow=True) # Required for Serverless compute
            .start())


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
