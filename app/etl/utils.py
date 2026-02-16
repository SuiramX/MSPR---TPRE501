import logging
import sys

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("ETL")

logger = setup_logging()

def validate_columns(df, required_cols, table_name):
    missing = [col for col in required_cols if col not in df.columns]
    if missing:
        logger.warning(f"Table {table_name}: Missing expected columns {missing}")
        return False
    return True
