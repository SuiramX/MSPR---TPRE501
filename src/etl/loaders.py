import pandas as pd
from sqlalchemy import create_engine
from .utils import logger

def get_engine(db_url):
    """Crée et retourne un moteur de connexion SQLAlchemy."""
    return create_engine(db_url)

def load_data(df, table_name, engine, if_exists="append"):
    """
    Charge un DataFrame dans une table PostgreSQL.
    Par défaut, les données sont ajoutées (append) à la table existante.
    """
    if df.empty:
        logger.warning(f"Skipping {table_name}: DataFrame is empty.")
        return

    try:
        logger.info(f"Loading {len(df)} rows into table '{table_name}'...")
        # Insertion en base de données via la méthode to_sql de pandas
        df.to_sql(table_name, engine, if_exists=if_exists, index=False)
        logger.info(f"Successfully loaded {table_name}.")
    except Exception as e:
        logger.error(f"Error loading {table_name}: {e}")
