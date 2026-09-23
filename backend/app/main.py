from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import operators, machines, tasks, telemetry, analytics
from app.database import engine, Base

# Create DB tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Operator Assistant API")

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(operators.router)
app.include_router(machines.router)
app.include_router(tasks.router)
app.include_router(telemetry.router)
app.include_router(analytics.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Operator Assistant API"}
