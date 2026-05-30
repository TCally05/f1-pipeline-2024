import os
from sqlalchemy import create_engine

DB_PATH = os.path.join("data", "f1_2024.db")

def get_engine():
    os.makedirs("data", exist_ok=True)
    return create_engine(f"sqlite:///{DB_PATH}")

def load_table(df, table_name):
    print(f"Loading {table_name} to database...")
    df.to_sql(table_name, get_engine(), if_exists="replace", index=False)
    print(f"  Loaded {len(df)} rows into table: {table_name}")
