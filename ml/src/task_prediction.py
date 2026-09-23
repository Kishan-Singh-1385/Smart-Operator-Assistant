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

def generate_synthetic_data(num_samples=1000):
    """Generate synthetic task data based on provided seed examples."""
    np.random.seed(42)
    
    task_types = ["Earth Excavation", "Trenching", "Material Loading", "Grading", "Demolition"]
    weathers = ["Sunny", "Rainy", "Cloudy", "Windy"]
    skill_levels = ["Beginner", "Intermediate", "Expert"]
    
    data = {
        "task_type": np.random.choice(task_types, num_samples),
        "weather": np.random.choice(weathers, num_samples),
        "operator_skill": np.random.choice(skill_levels, num_samples),
        "machine_age": np.random.randint(1, 15, num_samples),
        "estimated_time": np.random.uniform(20, 120, num_samples)
    }
    
    df = pd.DataFrame(data)
    
    # Simulate actual_time based on features (synthetic relationship)
    # E.g., rainy weather adds time, expert skill reduces time, older machine adds time
    weather_multiplier = {"Sunny": 1.0, "Cloudy": 1.05, "Windy": 1.1, "Rainy": 1.2}
    skill_multiplier = {"Expert": 0.9, "Intermediate": 1.0, "Beginner": 1.2}
    
    actual_times = []
    for _, row in df.iterrows():
        base = row["estimated_time"]
        wm = weather_multiplier[row["weather"]]
        sm = skill_multiplier[row["operator_skill"]]
        age_penalty = 1.0 + (row["machine_age"] * 0.01) # 1% increase per year
        
        # Add some random noise
        noise = np.random.uniform(0.9, 1.1)
        
        actual_time = base * wm * sm * age_penalty * noise
        actual_times.append(round(actual_time, 2))
        
    df["actual_time"] = actual_times
    return df

def train_task_model():
    """Train the RandomForest model on synthetic data."""
    print("Generating synthetic task data...")
    df = generate_synthetic_data(2000)
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # Save training data for reference
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    df.to_csv(os.path.join(data_dir, "task_training_data.csv"), index=False)
    
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
