from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(prefix="/foods", tags=["Foods"])


@router.get("/", response_model=List[schemas.FoodRead])
def get_foods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Food).offset(skip).limit(limit).all()


@router.get("/{food_id}", response_model=schemas.FoodRead)
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(models.Food).filter(models.Food.id_food == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@router.post("/", response_model=schemas.FoodRead, status_code=201)
def create_food(food: schemas.FoodCreate, db: Session = Depends(get_db)):
    db_food = models.Food(**food.model_dump())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food


@router.put("/{food_id}", response_model=schemas.FoodRead)
def update_food(food_id: int, food: schemas.FoodUpdate, db: Session = Depends(get_db)):
    db_food = db.query(models.Food).filter(models.Food.id_food == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    for field, value in food.model_dump(exclude_unset=True).items():
        setattr(db_food, field, value)
    db.commit()
    db.refresh(db_food)
    return db_food


@router.delete("/{food_id}", status_code=204)
def delete_food(food_id: int, db: Session = Depends(get_db)):
    db_food = db.query(models.Food).filter(models.Food.id_food == food_id).first()
    if not db_food:
        raise HTTPException(status_code=404, detail="Food not found")
    db.delete(db_food)
    db.commit()
