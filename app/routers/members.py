from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas

router = APIRouter(prefix="/members", tags=["Members"])


@router.get("/", response_model=List[schemas.MemberRead])
def get_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Member).offset(skip).limit(limit).all()


@router.get("/{member_id}", response_model=schemas.MemberRead)
def get_member(member_id: int, db: Session = Depends(get_db)):
    member = db.query(models.Member).filter(models.Member.id_member == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    return member


@router.post("/", response_model=schemas.MemberRead, status_code=201)
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    db_member = models.Member(**member.model_dump())
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.put("/{member_id}", response_model=schemas.MemberRead)
def update_member(member_id: int, member: schemas.MemberUpdate, db: Session = Depends(get_db)):
    db_member = db.query(models.Member).filter(models.Member.id_member == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    for field, value in member.model_dump(exclude_unset=True).items():
        setattr(db_member, field, value)
    db.commit()
    db.refresh(db_member)
    return db_member


@router.delete("/{member_id}", status_code=204)
def delete_member(member_id: int, db: Session = Depends(get_db)):
    db_member = db.query(models.Member).filter(models.Member.id_member == member_id).first()
    if not db_member:
        raise HTTPException(status_code=404, detail="Member not found")
    db.delete(db_member)
    db.commit()
