import pandas as pd
from sqlalchemy import create_engine
from .utils import logger

def get_engine(db_url):
    return create_engine(db_url)

def load_data(df, table_name, engine, if_exists="append"):
    if df.empty:
        logger.warning(f"Skipping {table_name}: DataFrame is empty.")
        return

    try:
        logger.info(f"Loading {len(df)} rows into table '{table_name}'...")
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        logger.info(f"Successfully loaded {table_name}.")
    except Exception as e:
        logger.error(f"Error loading {table_name}: {e}")
