# Smart Operator Assistant for CAT Machinery

This is the end-to-end hackathon prototype for a Smart Operator Assistant for CAT construction machinery.

## Architecture

The system demonstrates the intelligence loop:
**Observe → Analyze → Predict → Alert → Recommend**

- **Frontend:** React + Vite + Tailwind CSS + Recharts
- **Backend:** FastAPI + Python
- **Database:** PostgreSQL (Local)
- **ML & Intelligence:** Scikit-learn (RandomForest, IsolationForest)

## Folder Structure

```
smart-operator-assistant/
├── frontend/                # React application and dashboard
├── backend/                 # FastAPI REST API and SQLAlchemy models
├── ml/                      # Machine learning scripts and models
├── database/                # Database initialization scripts
├── README.md                # This file
└── .env.example             # Template for environment variables
```



## PostgreSQL Setup

1. Install PostgreSQL on your local machine.
2. Create a new database named `smart_operator_db`.
3. Create a `.env` file in the project root by copying `.env.example`:
   ```bash
   cp .env.example .env
   ```
4. Update the `DATABASE_URL` in your `.env` with your actual PostgreSQL credentials.
5. Initialize the database schema and seed data by running the seed script (see Backend Setup).

## Backend Setup

1. Open a terminal in the root directory.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   ```bash
   # Windows
   .venv\Scripts\activate
   # Mac/Linux
   source .venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
5. Seed the database (make sure your `.env` is configured):
   ```bash
   python backend/seed.py
   ```
6. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --app-dir backend --port 8001 --reload
   ```
   The API will be available at `http://localhost:8001`.

## ML Model Training

> **Note:** The problem statement provided an extremely small dataset. We have populated 1000 records of synthetic training data for task completion and telemetry analysis. These are stored statically in `ml/data/task_training_data.csv` and `ml/data/telemetry_training_data.csv`. You can freely modify these CSV files with your own data.

Run the ML training scripts (ensure the virtual environment is activated) to train the models on the CSV data:
```bash
python ml/src/task_prediction.py
python ml/src/anomaly_detection.py
```
This will generate the `.joblib` model files required by the backend.

## Frontend Setup

1. Open a new terminal in the `frontend/` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The Dashboard will be available at `http://localhost:5173`.

## Demo Workflow

1. **Dashboard Load:** Open the dashboard to see Operator `OP1001` and Machine `EXC001`. The current telemetry and active tasks will be displayed.
2. **Normal Operation:** The system monitors standard telemetry (idling, seatbelt fastened, no safety alerts).
3. **Anomaly & Safety Trigger:** When a simulated unsafe telemetry event is posted (e.g., via the `/api/telemetry` endpoint with seatbelt unfastened and high idling), the ML engine will detect an anomaly, the safety score will drop, and training recommendations (e.g., "Seatbelt Safety Training") will be generated.
4. **Task Prediction:** The dashboard can predict task completion time based on weather, operator skill, and machine age.

## API Endpoints

- `GET /api/operators`: List all operators
- `GET /api/operators/{id}`: Get operator details
- `GET /api/machines`: List all machines
- `GET /api/tasks`: List tasks
- `GET /api/telemetry/{machine_id}`: Get recent telemetry
- `POST /api/telemetry`: Submit new telemetry data
- `GET /api/training/recommendations/{operator_id}`: Get training recommendations
- `POST /api/predict/task-time`: Predict task completion time
- `POST /api/detect/anomaly`: Detect anomalous machine behavior

Explore all endpoints interactively at `http://localhost:8000/docs`.

## Future Improvements

- Replace synthetic data with historical IoT data.
- Integrate real-time WebSocket telemetry streams.
- Add robust authentication and authorization.
- Containerize with Docker for easier deployment.
