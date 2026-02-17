import pandas as pd
import os
from etl.loaders import get_engine
from etl.config import DB_URL
from etl.utils import logger

def export_cleaned_data():
    output_dir = "cleaned_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    tables = ["Food", "Exercise", "Member", "Workout", "Plan"]
    engine = get_engine(DB_URL)

    logger.info(f"Exporting cleaned data to {output_dir}/...")

    for table in tables:
        try:
            df = pd.read_sql_table(table, engine)
            output_path = os.path.join(output_dir, f"{table.lower()}_cleaned.csv")
            df.to_csv(output_path, index=False)
            logger.info(f"Exported {table} to {output_path} ({len(df)} rows)")
        except Exception as e:
            logger.error(f"Failed to export {table}: {e}")

if __name__ == "__main__":
    export_cleaned_data()
