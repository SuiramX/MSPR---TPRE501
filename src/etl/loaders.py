from sqlalchemy import text, create_engine
from etl.utils import logger

def get_engine(db_url):
    """Crée et retourne un moteur de connexion SQLAlchemy."""
    return create_engine(db_url)

def load_data(df, table_name, engine, truncate=False):
    """
    Charge un DataFrame dans une table PostgreSQL.
    Si truncate=True, vide la table avant l'insertion pour éviter les doublons.
    """
    if df.empty:
        logger.warning(f"Skipping {table_name}: DataFrame is empty.")
        return

    try:
        if truncate:
            logger.info(f"Clearing existing data in table '{table_name}'...")
            with engine.begin() as conn:
                # Utilisation de DELETE plutôt que TRUNCATE pour une gestion plus souple des verrous
                conn.execute(text(f'DELETE FROM "{table_name}"'))

        logger.info(f"Loading {len(df)} rows into table '{table_name}'...")
        # Insertion en base de données via la méthode to_sql de pandas
        # On utilise if_exists="append" car le DELETE a déjà fait le ménage
        df.to_sql(table_name, engine, if_exists="append", index=False)
        logger.info(f"Successfully loaded {table_name}.")
    except Exception as e:
        logger.error(f"Error loading {table_name}: {e}")
        raise e # On relance l'exception pour que l'orchestrateur puisse la capturer
