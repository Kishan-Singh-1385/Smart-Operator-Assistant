from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models
from app.schemas import schemas
from app.services.safety_service import process_telemetry_and_safety

router = APIRouter(
    prefix="/api/telemetry",
    tags=["telemetry"]
)

@router.get("/{machine_id}", response_model=List[schemas.Telemetry])
def get_telemetry(machine_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    telemetry = db.query(models.MachineTelemetry).filter(
        models.MachineTelemetry.machine_id == machine_id
    ).order_by(models.MachineTelemetry.timestamp.desc()).offset(skip).limit(limit).all()
    return telemetry

@router.post("/")
def create_telemetry(telemetry: schemas.TelemetryCreate, db: Session = Depends(get_db)):
    result = process_telemetry_and_safety(db, telemetry)
    return result
