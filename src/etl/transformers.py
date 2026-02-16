import pandas as pd
import numpy as np
import re
from .utils import logger, validate_columns
from .config import FOOD_MAPPING, MEMBER_TRACKING_MAPPING, PLAN_MAPPING, SCHEMAS

def generic_transform(df, mapping, table_name):
    if df.empty:
        return pd.DataFrame()

    logger.info(f"Transforming {table_name} data...")
    
    df = df.rename(columns=mapping)
    
    df["ingested_at"] = pd.Timestamp.now()
    
    schema_cols = SCHEMAS.get(table_name, [])
    final_df = df[[c for c in schema_cols if c in df.columns]].copy()
    
    validate_columns(final_df, schema_cols, table_name)
    
    return final_df

def transform_food_data(df):
    if df.empty: return pd.DataFrame()
    
    if "food" in df.columns:
        df["food"] = df["food"].str.lower().str.strip().str.replace(r"\s+", " ", regex=True)

    df = generic_transform(df, FOOD_MAPPING, "Food")
    
    numeric_cols = ["calories", "fats", "carbohydrates", "proteins", "fiber", "sodium", "sugar"]
    for col in [c for c in numeric_cols if c in df.columns]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(df[col].median())
        Q1, Q3 = df[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        df[col] = df[col].clip(Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
        if col == "calories": df[col] = df[col].clip(lower=0)

    logger.info(f"Food data ready: {df.shape}")
    return df

def transform_exercises(data_list):
    if not data_list: return pd.DataFrame()

    logger.info("Processing exercises...")
    exercises = [{
        "id_exercise": item.get("name"), 
        "name": item.get("name"),
        "type": item.get("category"), 
        "muscle_group": item.get("primaryMuscles", [None])[0] if item.get("primaryMuscles") else None,
        "equipment": item.get("equipment"),
        "difficulty": item.get("level"),
        "instructions": " ".join(item.get("instructions", [])),
        "image_url": item.get("images", [None])[0] if item.get("images") else None,
        "source_file": item.get("source_file", "unknown")
    } for item in data_list]
    
    df = pd.DataFrame(exercises)
    return generic_transform(df, {}, "Exercise")

def transform_members_and_workouts(df):
    if df.empty: return pd.DataFrame(), pd.DataFrame()

    df = df.rename(columns=MEMBER_TRACKING_MAPPING)
    
    member_cols = ["age", "gender", "height", "weight", "bmi", "fat_percentage"]
    member_df = df.groupby(member_cols).agg({'source_file': 'first'}).reset_index()
    member_df["id_member"] = member_df.index + 1
    
    member_df = generic_transform(member_df, {}, "Member")
    
    merged_df = df.merge(member_df, on=member_cols, how="left", suffixes=('', '_member'))
    workout_df = generic_transform(merged_df, {"id_member": "member_id"}, "Workout")

    logger.info(f"Transformed: {member_df.shape[0]} members, {workout_df.shape[0]} workouts.")
    return member_df, workout_df

def transform_plan_data(df):
    if df.empty: return pd.DataFrame()

    df = df.rename(columns=PLAN_MAPPING)

    def extract_indicators(row):
        exercise = str(row.get("recommended_exercise_plan", ""))
        meal = str(row.get("recommended_meal_plan", ""))
        
        steps = int(re.search(r"(\d+)\s*steps", exercise).group(1)) if re.search(r"(\d+)\s*steps", exercise) else 0
        style = re.split(r",?\s*(?:and\s+)?\d+\s*steps.*", exercise, flags=re.IGNORECASE)[0].strip()
        diet = re.split(r"\s+with\s+|:", meal)[0].strip() if re.split(r"\s+with\s+|:", meal) else meal
        protein = (re.search(r"(\w+\s*protein)", meal, re.IGNORECASE).group(1).lower().strip() 
                   if re.search(r"(\w+\s*protein)", meal, re.IGNORECASE) else "standard")
        
        return pd.Series([steps, style, diet, protein])

    df[["steps_target", "workout_style", "diet_category", "protein_tag"]] = df.apply(extract_indicators, axis=1)
    df["id_plan"] = df.index + 1

    return generic_transform(df, {}, "Plan")
