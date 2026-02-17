from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from security import verify_api_key
import models, schemas

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/", response_model=List[schemas.PlanRead])
def get_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Plan).offset(skip).limit(limit).all()


@router.get("/{plan_id}", response_model=schemas.PlanRead)
def get_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan


@router.post("/", response_model=schemas.PlanRead, status_code=201, dependencies=[Depends(verify_api_key)])
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    db_plan = models.Plan(**plan.model_dump())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.put("/{plan_id}", response_model=schemas.PlanRead, dependencies=[Depends(verify_api_key)])
def update_plan(plan_id: int, plan: schemas.PlanUpdate, db: Session = Depends(get_db)):
    db_plan = db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    for field, value in plan.model_dump(exclude_unset=True).items():
        setattr(db_plan, field, value)
    db.commit()
    db.refresh(db_plan)
    return db_plan


@router.delete("/{plan_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(models.Plan).filter(models.Plan.id_plan == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(db_plan)
    db.commit()
