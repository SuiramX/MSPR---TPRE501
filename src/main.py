import sys
from etl.extractors import extract_food_data, extract_exercises, extract_gym_members, extract_plan_data
from etl.transformers import (transform_food_data, transform_exercises, 
                              transform_members_and_workouts, transform_plan_data)
from etl.loaders import load_data, get_engine
from etl.config import DB_URL, DATA_DIR
from etl.utils import logger

def run_etl():
    logger.info("=== Starting Refactored ETL Pipeline ===")
    
    try:
        engine = get_engine(DB_URL)
        with engine.connect() as conn:
            logger.info("Database connection verified.")
    except Exception as e:
        logger.critical(f"Database connection failed: {e}")
        sys.exit(1)

    food_df = transform_food_data(extract_food_data(DATA_DIR))
    load_data(food_df, "Food", engine)
    
    exercise_df = transform_exercises(extract_exercises(DATA_DIR))
    load_data(exercise_df, "Exercise", engine)
    
    raw_tracking = extract_gym_members(DATA_DIR)
    member_df, workout_df = transform_members_and_workouts(raw_tracking)
    load_data(member_df, "Member", engine)
    load_data(workout_df, "Workout", engine)

    plan_df = transform_plan_data(extract_plan_data(DATA_DIR))
    load_data(plan_df, "Plan", engine)

    logger.info("=== ETL Pipeline Finished ===")

if __name__ == "__main__":
    run_etl()
