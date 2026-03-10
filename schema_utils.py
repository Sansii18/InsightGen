import pandas as pd


def extract_schema(df: pd.DataFrame) -> dict:
    """Return a mapping of column names to SQL-friendly data types.

    SQLite uses dynamic typing, but we convert pandas dtypes to approximate
    SQL types for the LLM prompt. The returned dict can be used for other
    purposes as well.
    """
    dtype_map = {}
    for col, dtype in df.dtypes.items():
        if pd.api.types.is_integer_dtype(dtype):
            dtype_map[col] = "INTEGER"
        elif pd.api.types.is_float_dtype(dtype):
            dtype_map[col] = "REAL"
        elif pd.api.types.is_bool_dtype(dtype):
            dtype_map[col] = "BOOLEAN"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            dtype_map[col] = "DATE"
        else:
            dtype_map[col] = "TEXT"
    return dtype_map


def generate_schema_string(df: pd.DataFrame, table_name: str = "dataset") -> str:
    """Produce a nicely formatted schema description string for the LLM prompt.

    Example output::

        Table: dataset
        columns:
        product_name (TEXT)
        price (REAL)
        order_date (DATE)
    """
    schema = extract_schema(df)
    lines = [f"Table: {table_name}", "columns:"]
    for col, typ in schema.items():
        lines.append(f"{col} ({typ})")
    return "\n".join(lines)
