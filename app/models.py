from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Member(Base):
    __tablename__ = "Member"

    id_member = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    gender = Column(String(50))
    height = Column(Float)
    weight = Column(Float)
    bmi = Column(Float)
    fat_percentage = Column(Float)
    source_file = Column(String(255))
    ingested_at = Column(TIMESTAMP, server_default=func.now())

    workouts = relationship("Workout", back_populates="member")


class Food(Base):
    __tablename__ = "Food"

    id_food = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    category = Column(String(100))
    calories = Column(Float)
    proteins = Column(Float)
    carbohydrates = Column(Float)
    fats = Column(Float)
    fiber = Column(Float)
    sodium = Column(Float)
    sugar = Column(Float)
    source_file = Column(String(255))
    ingested_at = Column(TIMESTAMP, server_default=func.now())


class Exercise(Base):
    __tablename__ = "Exercise"

    id_exercise = Column(String(100), primary_key=True, index=True)
    name = Column(String(255))
    type = Column(String(50))
    muscle_group = Column(String(100))
    equipment = Column(String(100))
    difficulty = Column(String(50))
    instructions = Column(Text)
    image_url = Column(Text)
    source_file = Column(String(255))
    ingested_at = Column(TIMESTAMP, server_default=func.now())


class Workout(Base):
    __tablename__ = "Workout"

    id_workout = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("Member.id_member"))
    workout_type = Column(String(100))
    session_duration = Column(Float)
    calories_burned = Column(Float)
    workout_frequency = Column(Integer)
    experience_level = Column(String(50))
    source_file = Column(String(255))
    ingested_at = Column(TIMESTAMP, server_default=func.now())

    member = relationship("Member", back_populates="workouts")


class Plan(Base):
    __tablename__ = "Plan"

    id_plan = Column(Integer, primary_key=True, index=True)
    gender = Column(String(50))
    goal = Column(String(100))
    bmi_category = Column(String(50))
    recommended_exercise_plan = Column(Text)
    recommended_meal_plan = Column(Text)
    steps_target = Column(Integer)
    workout_style = Column(String(100))
    diet_category = Column(String(100))
    protein_tag = Column(String(100))
    source_file = Column(String(255))
    ingested_at = Column(TIMESTAMP, server_default=func.now())
