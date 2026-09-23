import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "anomaly_detection_model.joblib")

def generate_synthetic_telemetry(num_samples=1000):
    """Generate synthetic telemetry data with normal and abnormal patterns."""
    np.random.seed(42)
    
    # Normal behavior (majority)
    normal_samples = int(num_samples * 0.9)
    normal_data = {
        "engine_hours": np.random.uniform(100, 5000, normal_samples),
        "fuel_used": np.random.uniform(2.0, 8.0, normal_samples),
        "load_cycles": np.random.randint(5, 20, normal_samples),
        "idling_time": np.random.uniform(0, 30, normal_samples),
        "seatbelt_status": [1] * normal_samples, # 1 for Fastened
        "safety_alert": [0] * normal_samples # 0 for False
    }
    
    # Abnormal behavior (minority)
    abnormal_samples = num_samples - normal_samples
    abnormal_data = {
        "engine_hours": np.random.uniform(100, 5000, abnormal_samples),
        "fuel_used": np.random.uniform(8.0, 20.0, abnormal_samples), # High fuel
        "load_cycles": np.random.randint(0, 5, abnormal_samples),   # Low cycles
        "idling_time": np.random.uniform(45, 120, abnormal_samples), # High idle
        "seatbelt_status": [0] * abnormal_samples, # 0 for Unfastened
        "safety_alert": [1] * abnormal_samples # 1 for True
    }
    
    df_normal = pd.DataFrame(normal_data)
    df_abnormal = pd.DataFrame(abnormal_data)
    
    df = pd.concat([df_normal, df_abnormal], ignore_index=True)
    return df

def train_anomaly_model():
    """Train Isolation Forest on synthetic telemetry."""
    print("Generating synthetic telemetry data...")
    df = generate_synthetic_telemetry(2000)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, "telemetry_training_data.csv"), index=False)
    
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
