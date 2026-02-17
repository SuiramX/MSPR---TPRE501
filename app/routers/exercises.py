from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from security import verify_api_key
import models, schemas

router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.get("/", response_model=List[schemas.ExerciseRead])
def get_exercises(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Exercise).offset(skip).limit(limit).all()


@router.get("/{exercise_id}", response_model=schemas.ExerciseRead)
def get_exercise(exercise_id: str, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.id_exercise == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


@router.post("/", response_model=schemas.ExerciseRead, status_code=201, dependencies=[Depends(verify_api_key)])
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Exercise).filter(models.Exercise.id_exercise == exercise.id_exercise).first()
    if existing:
        raise HTTPException(status_code=409, detail="Exercise already exists")
    db_exercise = models.Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@router.put("/{exercise_id}", response_model=schemas.ExerciseRead, dependencies=[Depends(verify_api_key)])
def update_exercise(exercise_id: str, exercise: schemas.ExerciseUpdate, db: Session = Depends(get_db)):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id_exercise == exercise_id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    for field, value in exercise.model_dump(exclude_unset=True).items():
        setattr(db_exercise, field, value)
    db.commit()
    db.refresh(db_exercise)
    return db_exercise


@router.delete("/{exercise_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_exercise(exercise_id: str, db: Session = Depends(get_db)):
    db_exercise = db.query(models.Exercise).filter(models.Exercise.id_exercise == exercise_id).first()
    if not db_exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(db_exercise)
    db.commit()
