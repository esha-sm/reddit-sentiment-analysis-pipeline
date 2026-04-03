import duckdb

with duckdb.connect("warehouse.db") as con:
    con.execute("""
    CREATE OR REPLACE TABLE fact_comments AS
    SELECT * 
    FROM read_parquet('data-lake/reddit/processed/fact_comments.parquet')
    """)