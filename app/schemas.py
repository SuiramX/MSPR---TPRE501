from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ─── Member ───────────────────────────────────────────────────────────────────

class MemberBase(BaseModel):
    age: Optional[int] = None
    gender: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    bmi: Optional[float] = None
    fat_percentage: Optional[float] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(MemberBase):
    pass

class MemberRead(MemberBase):
    id_member: int
    source_file: Optional[str] = None
    ingested_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Food ─────────────────────────────────────────────────────────────────────

class FoodBase(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    calories: Optional[float] = None
    proteins: Optional[float] = None
    carbohydrates: Optional[float] = None
    fats: Optional[float] = None
    fiber: Optional[float] = None
    sodium: Optional[float] = None
    sugar: Optional[float] = None

class FoodCreate(FoodBase):
    pass

class FoodUpdate(FoodBase):
    pass

class FoodRead(FoodBase):
    id_food: int
    source_file: Optional[str] = None
    ingested_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Exercise ─────────────────────────────────────────────────────────────────

class ExerciseBase(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    muscle_group: Optional[str] = None
    equipment: Optional[str] = None
    difficulty: Optional[str] = None
    instructions: Optional[str] = None
    image_url: Optional[str] = None

class ExerciseCreate(ExerciseBase):
    id_exercise: str

class ExerciseUpdate(ExerciseBase):
    pass

class ExerciseRead(ExerciseBase):
    id_exercise: str
    source_file: Optional[str] = None
    ingested_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Workout ──────────────────────────────────────────────────────────────────

class WorkoutBase(BaseModel):
    member_id: Optional[int] = None
    workout_type: Optional[str] = None
    session_duration: Optional[float] = None
    calories_burned: Optional[float] = None
    workout_frequency: Optional[int] = None
    experience_level: Optional[str] = None

class WorkoutCreate(WorkoutBase):
    pass

class WorkoutUpdate(WorkoutBase):
    pass

class WorkoutRead(WorkoutBase):
    id_workout: int
    source_file: Optional[str] = None
    ingested_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ─── Plan ─────────────────────────────────────────────────────────────────────

class PlanBase(BaseModel):
    gender: Optional[str] = None
    goal: Optional[str] = None
    bmi_category: Optional[str] = None
    recommended_exercise_plan: Optional[str] = None
    recommended_meal_plan: Optional[str] = None
    steps_target: Optional[int] = None
    workout_style: Optional[str] = None
    diet_category: Optional[str] = None
    protein_tag: Optional[str] = None

class PlanCreate(PlanBase):
    pass

class PlanUpdate(PlanBase):
    pass

class PlanRead(PlanBase):
    id_plan: int
    source_file: Optional[str] = None
    ingested_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
