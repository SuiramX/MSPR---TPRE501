-- Initial database setup
-- Tables will be created here
CREATE TABLE IF NOT EXISTS "Plan" (
    id_plan SERIAL PRIMARY KEY,
    gender VARCHAR(50),
    goal VARCHAR(100),
    bmi_category VARCHAR(50),
    recommended_exercise_plan TEXT,
    recommended_meal_plan TEXT,
    steps_target INT,
    workout_style VARCHAR(100),
    diet_category VARCHAR(100),
    protein_tag VARCHAR(100),
    source_file VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Exercise" (
    id_exercise VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50),
    muscle_group VARCHAR(100),
    equipment VARCHAR(100),
    difficulty VARCHAR(50),
    instructions TEXT,
    image_url TEXT,
    source_file VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Member" (
    id_member SERIAL PRIMARY KEY,
    age INT,
    gender VARCHAR(50),
    height FLOAT,
    weight FLOAT,
    bmi FLOAT,
    fat_percentage FLOAT,
    source_file VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Food" (
    id_food SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    calories FLOAT,
    proteins FLOAT,
    carbohydrates FLOAT,
    fats FLOAT,
    fiber FLOAT,
    sodium FLOAT,
    sugar FLOAT,
    source_file VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "Workout" (
    id_workout SERIAL PRIMARY KEY,
    member_id INT, -- Implicit relation
    workout_type VARCHAR(100),
    session_duration FLOAT,
    calories_burned FLOAT,
    workout_frequency INT,
    experience_level VARCHAR(50),
    source_file VARCHAR(255),
    ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES "Member"(id_member)
);
