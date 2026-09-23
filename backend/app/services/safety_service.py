from sqlalchemy.orm import Session
from app.models import models
from app.schemas import schemas
import sys
import os

# Add ml folder to path to import safety engine
ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml"))
if ml_path not in sys.path:
    sys.path.append(ml_path)

from src.safety_engine import evaluate_safety

def process_telemetry_and_safety(db: Session, telemetry_data: schemas.TelemetryCreate):
    # Save telemetry
    db_telemetry = models.MachineTelemetry(**telemetry_data.model_dump())
    db.add(db_telemetry)
    
    # Evaluate safety
    safety_result = evaluate_safety(telemetry_data.model_dump())
    
    # Update operator score (simplified running average or direct replacement for prototype)
    operator = db.query(models.Operator).filter(models.Operator.operator_id == telemetry_data.operator_id).first()
    if operator:
        # Simple prototype logic: update current score based on recent event
        operator.safety_score = (operator.safety_score + safety_result["safety_score"]) / 2
        
    # Log safety events if high risk
    if safety_result["risk_level"] in ["MEDIUM RISK", "HIGH RISK"]:
        for reason in safety_result["reasons"]:
            event = models.SafetyEvent(
                operator_id=telemetry_data.operator_id,
                machine_id=telemetry_data.machine_id,
                event_type=reason,
                severity=safety_result["risk_level"],
                description=f"{reason} detected via telemetry."
            )
            db.add(event)
            
    db.commit()
    
    return {
        "telemetry_saved": True,
        "safety_analysis": safety_result
    }
