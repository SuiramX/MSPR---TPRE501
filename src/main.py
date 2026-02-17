import sys
from etl.extractors import extract_food_data, extract_exercises, extract_gym_members, extract_plan_data
from etl.transformers import (transform_food_data, transform_exercises, 
                              transform_members_and_workouts, transform_plan_data)
from etl.loaders import load_data, get_engine
from etl.config import DB_URL, DATA_DIR
from etl.utils import logger
import datetime

from sqlalchemy import text

def log_job(engine, status, details=None):
    """Log l'état d'exécution du pipeline dans la table 'etl_logs'."""
    try:
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO etl_logs (job_name, status, details) VALUES (:job_name, :status, :details)"),
                {"job_name": "Full ETL", "status": status, "details": details}
            )
    except Exception as e:
        logger.error(f"Failed to log job status to DB: {e}")

def run_etl():
    """
    Fonction principale orchestrant le pipeline ETL :
    1. Connexion à la base de données.
    2. Extraction et Transformation de chaque source.
    3. Chargement des données transformées en base.
    4. Gestion des erreurs et journalisation.
    """
    logger.info("=== Starting Refactored ETL Pipeline ===")
    
    try:
        engine = get_engine(DB_URL)
        with engine.connect() as conn:
            logger.info("Database connection verified.")
    except Exception as e:
        logger.critical(f"Database connection failed: {e}")
        return False

    log_job(engine, "STARTED")
    
    try:
        # Pipeline Nutrition
        food_df = transform_food_data(extract_food_data(DATA_DIR))
        load_data(food_df, "Food", engine)
        
        # Pipeline Exercices
        exercise_df = transform_exercises(extract_exercises(DATA_DIR))
        load_data(exercise_df, "Exercise", engine)
        
        # Pipeline Membres et Entraînements
        raw_tracking = extract_gym_members(DATA_DIR)
        member_df, workout_df = transform_members_and_workouts(raw_tracking)
        load_data(member_df, "Member", engine)
        load_data(workout_df, "Workout", engine)

        # Pipeline Plans Personnalisés
        plan_df = transform_plan_data(extract_plan_data(DATA_DIR))
        load_data(plan_df, "Plan", engine)

        logger.info("=== ETL Pipeline Finished ===")
        log_job(engine, "SUCCESS")
        return True
    except Exception as e:
        logger.error(f"ETL Pipeline failed: {e}")
        log_job(engine, "FAILED", str(e))
        return False

if __name__ == "__main__":
    run_etl()
