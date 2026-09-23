from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
import sys
import os

from app.database import get_db
from app.models import models
from app.schemas import schemas

# Add ml folder to path
ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml"))
if ml_path not in sys.path:
    sys.path.append(ml_path)

from src.task_prediction import predict_task_time
from src.anomaly_detection import detect_anomaly

router = APIRouter(
    tags=["analytics"]
)

class TaskPredictionRequest(BaseModel):
    task_type: str
    weather: str
    operator_skill: str
    machine_age: int
    estimated_time: float

class AnomalyDetectionRequest(BaseModel):
    engine_hours: float
    fuel_used: float
    load_cycles: int
    idling_time: float
    seatbelt_status: str
    safety_alert: bool

@router.post("/api/detect/anomaly", response_model=schemas.AnomalyResponse)
def detect_machine_anomaly(request: AnomalyDetectionRequest):
    try:
        result = detect_anomaly(
            request.engine_hours,
            request.fuel_used,
            request.load_cycles,
            request.idling_time,
            request.seatbelt_status,
            request.safety_alert
        )
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection error: {str(e)}")

class TaskPredictionRequest(BaseModel):
    task_type: str
    weather: str
    operator_skill: str
    machine_age: int
    estimated_time: float

@router.post("/api/predict/task-time", response_model=schemas.PredictionResponse)
def predict_time(request: TaskPredictionRequest):
    try:
        result = predict_task_time(
            request.task_type,
            request.weather,
            request.operator_skill,
            request.machine_age,
            request.estimated_time
        )
        return result
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@router.get("/api/analytics/operator/{operator_id}")
def get_operator_analytics(operator_id: str, db: Session = Depends(get_db)):
    operator = db.query(models.Operator).filter(models.Operator.operator_id == operator_id).first()
    if not operator:
        raise HTTPException(status_code=404, detail="Operator not found")
        
    tasks = db.query(models.Task).filter(models.Task.operator_id == operator_id).all()
    completed_tasks = [t for t in tasks if t.status == "Completed"]
    
    return {
        "operator_id": operator_id,
        "safety_score": operator.safety_score,
        "efficiency_score": operator.efficiency_score,
        "total_tasks_assigned": len(tasks),
        "tasks_completed": len(completed_tasks)
    }

from app.services.recommendation_service import get_operator_recommendations

@router.get("/api/training/recommendations/{operator_id}", response_model=List[schemas.TrainingRecommendation])
def get_recommendations(operator_id: str, db: Session = Depends(get_db)):
    try:
        recs = get_operator_recommendations(db, operator_id)
        return recs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
