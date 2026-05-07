from pyspark.sql.functions import col, date_sub, current_date, regexp_replace, lower, trim

def validate_not_null(df, columns):
    """Filters out rows where mandatory columns are NULL."""
    cols_to_check = [columns] if isinstance(columns, str) else columns
    for c in cols_to_check:
        df = df.filter(col(c).isNotNull())
    return df

def clean_phone_number(df, column_name, new_column_name):
    """
    Removes all non-numeric characters (symbols, dots, letters, etc.) 
    from a phone number column and transforms it to an integer (LongType).
    Keeps the original column and creates a new one.
    """
    return df.withColumn(
        new_column_name,
        regexp_replace(col(column_name), r"[^0-9]", "").cast("long")
    )

def clean_website_url(df, column_name, new_column_name):
    """
    Standardizes website URLs by:
    1. Trimming spaces and converting to lowercase.
    2. Keeping protocols (http, https) and 'www' if present.
    3. Removing truly invalid characters (keeps alphanumeric, dots, hyphens, slashes, and colons).
    Keeps the original column and creates a new one.
    """
    # Regex to remove characters that are noise or invalid symbols in a basic URL 
    # We keep ':' and '/' to preserve the 'http://' prefix and path structure.
    # We keep '.' to preserve 'www.' and domain extensions.
    regex_invalid_chars = r"[^a-zA-Z0-9\.\-\/:]"
    
    return df.withColumn(
        new_column_name,
        regexp_replace(lower(trim(col(column_name))), regex_invalid_chars, "")
    )


