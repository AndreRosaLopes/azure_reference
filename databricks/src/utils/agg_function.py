import pyspark.sql.functions as F

def apply_aggregation(df, agg_by=None, metrics=None):
    """
    Applies dynamic aggregations to a DataFrame.
    
    :param df: Input PySpark DataFrame
    :param agg_by: List of column names to group by. Example: ["state", "country"]
    :param metrics: List of tuples/lists defining the aggregations. 
                    Format: [(alias_name, column_name, function_name), ...]
                    Example: [("total_sales", "amount", "sum"), ("count_users", "id", "count")]
    """
    agg_by = agg_by or []
    metrics = metrics or []
    
    func_map = {
        "count": F.count,
        "sum": F.sum,
        "avg": F.avg,
        "min": F.min,
        "max": F.max
    }
    
    agg_exprs = []
    for alias_name, col_name, func_name in metrics:
        spark_func = func_map.get(func_name.lower())
        if spark_func:
            agg_exprs.append(spark_func(F.col(col_name)).alias(alias_name))
        else:
            raise ValueError(f"Unsupported aggregation function: {func_name}")
            
    if agg_by and agg_exprs:
        return df.groupBy(*agg_by).agg(*agg_exprs)
        
    return df
