import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "anomaly_detection_model.joblib")

def train_anomaly_model():
    """Train Isolation Forest on the provided telemetry dataset."""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "telemetry_training_data.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
        
    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    print("Training IsolationForest...")
    # Contamination is the expected proportion of outliers
    model = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
    model.fit(df)
    
    joblib.dump(model, MODEL_PATH)
    print(f"Anomaly detection model saved to {MODEL_PATH}")

def detect_anomaly(engine_hours, fuel_used, load_cycles, idling_time, seatbelt_status_str, safety_alert_bool):
    """Detect if current telemetry is anomalous."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file not found. Run train_anomaly_model() first.")
        
    model = joblib.load(MODEL_PATH)
    
    seatbelt_val = 1 if seatbelt_status_str == "Fastened" else 0
    alert_val = 1 if safety_alert_bool else 0
    
    input_df = pd.DataFrame([{
        "engine_hours": engine_hours,
        "fuel_used": fuel_used,
        "load_cycles": load_cycles,
        "idling_time": idling_time,
        "seatbelt_status": seatbelt_val,
        "safety_alert": alert_val
    }])
    
    # Predict returns 1 for inliers, -1 for outliers
    prediction = model.predict(input_df)[0]
    
    # Score returns negative values for anomalies, positive for normal
    # We invert it for a simpler "anomaly score" (higher = more anomalous)
    raw_score = model.decision_function(input_df)[0]
    anomaly_score = -raw_score
    
    is_anomaly = prediction == -1
    
    reason = None
    if is_anomaly:
        reasons = []
        if fuel_used > 8.0: reasons.append("High fuel consumption")
        if idling_time > 45: reasons.append("Excessive idling")
        if seatbelt_val == 0: reasons.append("Seatbelt violation")
        if alert_val == 1: reasons.append("Safety alert triggered")
        if not reasons: reasons.append("Unusual operating pattern detected")
        reason = ", ".join(reasons)
        
    return {
        "anomaly": bool(is_anomaly),
        "anomaly_score": round(float(anomaly_score), 4),
        "reason": reason
    }

if __name__ == "__main__":
    train_anomaly_model()
