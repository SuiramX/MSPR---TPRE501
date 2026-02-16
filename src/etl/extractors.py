import pandas as pd
import glob
import json
import os
from .utils import logger

def extract_data_files(pattern, data_dir="data"):
    full_pattern = os.path.join(data_dir, pattern)
    all_files = glob.glob(full_pattern)
    df_list = []
    
    logger.info(f"Scanning for files: {pattern}")
    for filename in all_files:
        try:
            if filename.endswith(".csv"):
                df = pd.read_csv(filename)
            elif filename.endswith(".xlsx") or filename.endswith(".xls"):
                df = pd.read_excel(filename)
            else:
                continue

            df["source_file"] = os.path.basename(filename)
            
            df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
            df_list.append(df)
            logger.info(f"Loaded {os.path.basename(filename)} ({len(df)} rows)")
        except Exception as e:
            logger.error(f"Error reading {filename}: {e}")

    if not df_list:
        return pd.DataFrame()

    return pd.concat(df_list, ignore_index=True)

def extract_food_data(data_dir="data"):
    return extract_data_files("food_data_group*", data_dir)

def extract_exercises(data_dir="data"):
    json_path = os.path.join(data_dir, "exercises.json")
    if not os.path.exists(json_path):
        logger.warning(f"{json_path} not found.")
        return []
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Loaded {len(data)} exercises from JSON.")
        
        for item in data:
            item["source_file"] = "exercises.json"
            
        return data
    except Exception as e:
        logger.error(f"Error reading exercises.json: {e}")
        return []

def extract_gym_members(data_dir="data"):
    return extract_data_files("members_tracking*", data_dir)

def extract_plan_data(data_dir="data"):
    return extract_data_files("workout_plans*", data_dir)
