def create_table_if_not_exists(spark, table_name: str, schema: str):
    """
    Ensure a Delta table exists with the given schema.

    If the table already exists, this is a no-op.
    """
    spark.sql(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        {schema}
        USING DELTA
        """
    )