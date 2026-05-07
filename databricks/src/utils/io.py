def read_stream(spark, format="delta", path=None, table=None, options=None):
    """
    Generic function to read a streaming DataFrame.
    
    :param spark: SparkSession instance
    :param format: Source format (e.g., 'delta', 'cloudFiles')
    :param path: Storage path (if applicable)
    :param table: Table name (if applicable)
    :param options: Dictionary of format-specific options
    :return: Streaming PySpark DataFrame
    """
    options = options or {}
    reader = spark.readStream.format(format)
    
    for key, value in options.items():
        reader = reader.option(key, value)
        
    if path:
        return reader.load(path)
    elif table:
        return reader.table(table)
    else:
        raise ValueError("Either 'path' or 'table' must be provided to read_stream.")
