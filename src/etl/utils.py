import logging
import sys
import os

def setup_logging():
    """
    Configure le système de logging.
    Les logs sont affichés sur la console et sauvegardés dans 'logs/etl.log'.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join(log_dir, "etl.log"))
        ]
    )
    return logging.getLogger("ETL")

# Instance globale du logger pour tout le package ETL
logger = setup_logging()

def validate_columns(df, required_cols, table_name):
    """
    Vérifie si toutes les colonnes requises sont présentes dans le DataFrame.
    Affiche un avertissement si certaines colonnes manquent.
    """
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logger.warning(f"Table {table_name}: Missing expected columns {missing}")
        return False
    return True
