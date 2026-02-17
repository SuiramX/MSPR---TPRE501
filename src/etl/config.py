import os

DB_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/mspr")

DATA_DIR = "/data"

# Mapping pour harmoniser les noms de colonnes des données nutritionnelles
FOOD_MAPPING = {
    "Caloric Value": "calories",
    "Fat": "fats",
    "Carbohydrates": "carbohydrates",
    "Protein": "proteins",
    "Fiber": "fiber",
    "Sodium": "sodium",
    "Sugar": "sugar",
    "Category": "category",
    "food": "name"
}

# Mapping pour les données de suivi des membres (Gym Members)
MEMBER_TRACKING_MAPPING = {
    "Age": "age", 
    "Gender": "gender", 
    "Height (m)": "height", 
    "Weight (kg)": "weight", 
    "BMI": "bmi", 
    "Fat_Percentage": "fat_percentage",
    "Workout_Type": "workout_type",
    "Session_Duration (hours)": "session_duration",
    "Calories_Burned": "calories_burned",
    "Workout_Frequency (days/week)": "workout_frequency",
    "Experience_Level": "experience_level"
}

# Mapping pour les plans d'entraînement et d'alimentation
PLAN_MAPPING = {
    "Gender": "gender",
    "Goal": "goal",
    "BMI Category": "bmi_category",
    "Exercise Schedule": "recommended_exercise_plan",
    "Meal Plan": "recommended_meal_plan"
}

# Colonnes pour la traçabilité des données
TRACEABILITY_COLS = ["source_file", "ingested_at"]

# Définition des schémas cibles pour chaque table en base de données
SCHEMAS = {
    "Food": ["name", "category", "calories", "proteins", "carbohydrates", "fats", "fiber", "sodium", "sugar"] + TRACEABILITY_COLS,
    "Exercise": ["id_exercise", "name", "type", "muscle_group", "equipment", "difficulty", "instructions", "image_url"] + TRACEABILITY_COLS,
    "Member": ["id_member", "age", "gender", "height", "weight", "bmi", "fat_percentage"] + TRACEABILITY_COLS,
    "Workout": ["member_id", "workout_type", "session_duration", "calories_burned", "workout_frequency", "experience_level"] + TRACEABILITY_COLS,
    "Plan": ["id_plan", "gender", "goal", "bmi_category", "recommended_exercise_plan", "recommended_meal_plan", 
             "steps_target", "workout_style", "diet_category", "protein_tag"] + TRACEABILITY_COLS
}
