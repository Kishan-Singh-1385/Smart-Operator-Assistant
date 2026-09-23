import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import joblib
import os

MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODEL_DIR, "task_prediction_model.joblib")
ENCODERS_PATH = os.path.join(MODEL_DIR, "task_encoders.joblib")

def train_task_model():
    """Train the RandomForest model on the provided dataset."""
    data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "task_training_data.csv")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset not found at {data_path}")
        
    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    print("Encoding categorical features...")
    encoders = {}
    categorical_cols = ["task_type", "weather", "operator_skill"]
    
    for col in categorical_cols:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le
        
    X = df.drop("actual_time", axis=1)
    y = df["actual_time"]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training RandomForestRegressor...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    score = model.score(X_test, y_test)
    print(f"Model trained. Test R^2 Score: {score:.4f}")
    
    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoders, ENCODERS_PATH)
    print(f"Model saved to {MODEL_PATH}")

def predict_task_time(task_type, weather, operator_skill, machine_age, estimated_time):
    """Predict task completion time."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODERS_PATH):
        raise FileNotFoundError("Model files not found. Run train_task_model() first.")
        
    model = joblib.load(MODEL_PATH)
    encoders = joblib.load(ENCODERS_PATH)
    
    # Prepare input
    input_df = pd.DataFrame([{
        "task_type": task_type,
        "weather": weather,
        "operator_skill": operator_skill,
        "machine_age": machine_age,
        "estimated_time": estimated_time
    }])
    
    # Encode input safely
    for col in ["task_type", "weather", "operator_skill"]:
        if col in encoders:
            try:
                input_df[col] = encoders[col].transform(input_df[col])
            except ValueError:
                # Handle unseen category
                input_df[col] = 0
                
    prediction = model.predict(input_df)[0]
    
    # Mock confidence based on tree variance
    preds = np.array([tree.predict(input_df)[0] for tree in model.estimators_])
    std_dev = np.std(preds)
    
    # Inverse mapping of standard deviation to confidence percentage
    confidence = max(0, 100 - (std_dev / prediction * 100 * 2))
    
    return {
        "predicted_time": round(prediction, 2),
        "confidence": round(confidence, 1),
        "model_version": "1.0-synthetic"
    }

if __name__ == "__main__":
    train_task_model()
