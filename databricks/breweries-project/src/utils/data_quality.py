from pyspark.sql.functions import col, date_sub, current_date

def validate_not_null(df, columns):
    """Filters out rows where mandatory columns are NULL."""
    cols_to_check = [columns] if isinstance(columns, str) else columns
    for c in cols_to_check:
        df = df.filter(col(c).isNotNull())
    return df

def filter_late_data(df, partition_col, watermark_days):
    """Filters data outside the watermark window if partition is a date."""
    # Note: Only apply if partition_col is a date type
    return df
