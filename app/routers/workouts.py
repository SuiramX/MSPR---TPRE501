from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from security import verify_api_key
import models, schemas

router = APIRouter(prefix="/workouts", tags=["Workouts"])


@router.get("/", response_model=List[schemas.WorkoutRead])
def get_workouts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Workout).offset(skip).limit(limit).all()


@router.get("/{workout_id}", response_model=schemas.WorkoutRead)
def get_workout(workout_id: int, db: Session = Depends(get_db)):
    workout = db.query(models.Workout).filter(models.Workout.id_workout == workout_id).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout


@router.get("/member/{member_id}", response_model=List[schemas.WorkoutRead])
def get_workouts_by_member(member_id: int, db: Session = Depends(get_db)):
    return db.query(models.Workout).filter(models.Workout.member_id == member_id).all()


@router.post("/", response_model=schemas.WorkoutRead, status_code=201, dependencies=[Depends(verify_api_key)])
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(get_db)):
    if workout.member_id:
        member = db.query(models.Member).filter(models.Member.id_member == workout.member_id).first()
        if not member:
            raise HTTPException(status_code=404, detail="Member not found")
    db_workout = models.Workout(**workout.model_dump())
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.put("/{workout_id}", response_model=schemas.WorkoutRead, dependencies=[Depends(verify_api_key)])
def update_workout(workout_id: int, workout: schemas.WorkoutUpdate, db: Session = Depends(get_db)):
    db_workout = db.query(models.Workout).filter(models.Workout.id_workout == workout_id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    for field, value in workout.model_dump(exclude_unset=True).items():
        setattr(db_workout, field, value)
    db.commit()
    db.refresh(db_workout)
    return db_workout


@router.delete("/{workout_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_workout(workout_id: int, db: Session = Depends(get_db)):
    db_workout = db.query(models.Workout).filter(models.Workout.id_workout == workout_id).first()
    if not db_workout:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(db_workout)
    db.commit()
