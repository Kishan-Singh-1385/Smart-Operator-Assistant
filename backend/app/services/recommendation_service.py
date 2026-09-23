from sqlalchemy.orm import Session
from app.models import models
import sys
import os

ml_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../ml"))
if ml_path not in sys.path:
    sys.path.append(ml_path)

from src.recommendations import generate_training_recommendation
from src.safety_engine import evaluate_safety

def get_operator_recommendations(db: Session, operator_id: str):
    # Retrieve recent telemetry to assess current state (simplified for prototype)
    recent_telemetry = db.query(models.MachineTelemetry).filter(
        models.MachineTelemetry.operator_id == operator_id
    ).order_by(models.MachineTelemetry.timestamp.desc()).first()
    
    if not recent_telemetry:
        return []
        
    # In a full system, this would aggregate historical data and anomalies.
    # For prototype, evaluate recent telemetry for safety issues.
    telemetry_dict = {
        "seatbelt_status": recent_telemetry.seatbelt_status,
        "safety_alert": recent_telemetry.safety_alert,
        "idling_time": recent_telemetry.idling_time,
        "fuel_used": recent_telemetry.fuel_used,
        "engine_hours": recent_telemetry.engine_hours,
        "load_cycles": recent_telemetry.load_cycles
    }
    
    safety_result = evaluate_safety(telemetry_dict)
    
    # We could also call detect_anomaly here if desired.
    # For now, pass a dummy anomaly to demonstrate the integration if idling is very high.
    # We will rely on safety_result primarily.
    anomaly_mock = None
    if recent_telemetry.fuel_used > 8.0:
        anomaly_mock = {"anomaly": True, "reason": "High fuel consumption"}
        
    recommendations = generate_training_recommendation(safety_result, anomaly_mock)
    return recommendations
