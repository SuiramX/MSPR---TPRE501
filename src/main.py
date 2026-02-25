import sys
import time
from etl.extractors import extract_food_data, extract_exercises, extract_gym_members, extract_plan_data
from etl.transformers import (transform_food_data, transform_exercises, 
                              transform_members_and_workouts, transform_plan_data)
from etl.loaders import load_data, get_engine
from etl.config import DB_URL, DATA_DIR
from etl.utils import logger
import datetime
from sqlalchemy import text
from etl.metrics import ETL_JOB_DURATION, ETL_JOB_STATUS, ETL_JOB_FAILURES, ETL_JOB_LAST_SUCCESS

def run_etl():
    """
    Fonction principale orchestrant le pipeline ETL :
    1. Connexion à la base de données.
    2. Extraction et Transformation de chaque source.
    3. Chargement des données transformées en base.
    4. Gestion des erreurs et journalisation via Prometheus.
    """
    logger.info("=== Starting Refactored ETL Pipeline ===")
    
    # Démarrer le chrono pour le pipeline
    start_time = time.time()
    
    # Signaler que l'ETL est en cours (2)
    ETL_JOB_STATUS.set(2)
    
    try:
        engine = get_engine(DB_URL)
        with engine.connect() as conn:
            logger.info("Database connection verified.")
    except Exception as e:
        logger.critical(f"Database connection failed: {e}")
        ETL_JOB_STATUS.set(0)
        ETL_JOB_FAILURES.inc()
        # Enregistrer la durée même en cas d'échec
        ETL_JOB_DURATION.set(time.time() - start_time)
        return False

    try:
        # 1. Pipeline Nutrition
        food_df = transform_food_data(extract_food_data(DATA_DIR))
        load_data(food_df, "Food", engine, truncate=True)
        
        # 2. Pipeline Exercices
        exercise_df = transform_exercises(extract_exercises(DATA_DIR))
        load_data(exercise_df, "Exercise", engine, truncate=True)
        
        # 3. Pipeline Membres et Entraînements (Gestion de l'intégrité référentielle)
        raw_tracking = extract_gym_members(DATA_DIR)
        member_df, workout_df = transform_members_and_workouts(raw_tracking)
        
        # On vide d'abord les entraînements (Workout) pour pouvoir vider les membres (Member)
        # Mais on ne charge pas encore ! On prépare juste le terrain.
        from sqlalchemy import text
        with engine.begin() as conn:
            conn.execute(text('DELETE FROM "Workout"'))
            conn.execute(text('DELETE FROM "Member"'))
            
        load_data(member_df, "Member", engine, truncate=False) # Déjà vidé
        load_data(workout_df, "Workout", engine, truncate=False) # Déjà vidé

        # 4. Pipeline Plans Personnalisés
        plan_df = transform_plan_data(extract_plan_data(DATA_DIR))
        load_data(plan_df, "Plan", engine, truncate=True)

        logger.info("=== ETL Pipeline Finished ===")
        
        # Succès de l'ETL
        ETL_JOB_STATUS.set(1)
        ETL_JOB_LAST_SUCCESS.set(time.time())
        ETL_JOB_DURATION.set(time.time() - start_time)
        return True

    except Exception as e:
        logger.error(f"ETL Pipeline failed: {e}")
        
        # Echec de l'ETL
        ETL_JOB_STATUS.set(0)
        ETL_JOB_FAILURES.inc()
        ETL_JOB_DURATION.set(time.time() - start_time)
        return False

if __name__ == "__main__":
    run_etl()
