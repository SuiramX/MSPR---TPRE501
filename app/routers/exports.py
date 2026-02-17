import io
import pandas as pd
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import get_db
from security import verify_api_key
import models

router = APIRouter(prefix="/export", tags=["Export CSV"])

EXCLUDED_COLS = {"source_file", "ingested_at"}


def to_csv_response(records: list, filename: str) -> StreamingResponse:
    if not records:
        df = pd.DataFrame()
    else:
        df = pd.DataFrame([
            {k: v for k, v in row.__dict__.items() if not k.startswith("_") and k not in EXCLUDED_COLS}
            for row in records
        ])
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return StreamingResponse(
        iter([buffer.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@router.get("/members/csv", dependencies=[Depends(verify_api_key)])
def export_members(db: Session = Depends(get_db)):
    records = db.query(models.Member).all()
    return to_csv_response(records, "members.csv")


@router.get("/foods/csv", dependencies=[Depends(verify_api_key)])
def export_foods(db: Session = Depends(get_db)):
    records = db.query(models.Food).all()
    return to_csv_response(records, "foods.csv")


@router.get("/exercises/csv", dependencies=[Depends(verify_api_key)])
def export_exercises(db: Session = Depends(get_db)):
    records = db.query(models.Exercise).all()
    return to_csv_response(records, "exercises.csv")


@router.get("/workouts/csv", dependencies=[Depends(verify_api_key)])
def export_workouts(db: Session = Depends(get_db)):
    records = db.query(models.Workout).all()
    return to_csv_response(records, "workouts.csv")


@router.get("/plans/csv", dependencies=[Depends(verify_api_key)])
def export_plans(db: Session = Depends(get_db)):
    records = db.query(models.Plan).all()
    return to_csv_response(records, "plans.csv")
