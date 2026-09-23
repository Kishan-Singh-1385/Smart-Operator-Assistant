from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime

class OperatorBase(BaseModel):
    name: str
    skill_level: Optional[str] = None

class OperatorCreate(OperatorBase):
    operator_id: str

class Operator(OperatorBase):
    id: int
    operator_id: str
    safety_score: float
    efficiency_score: float

    model_config = ConfigDict(from_attributes=True)


class MachineBase(BaseModel):
    machine_type: str
    machine_age: Optional[int] = None
    engine_hours: Optional[float] = None
    status: Optional[str] = None

class MachineCreate(MachineBase):
    machine_id: str

class Machine(MachineBase):
    id: int
    machine_id: str

    model_config = ConfigDict(from_attributes=True)


class TaskBase(BaseModel):
    task_type: str
    weather: Optional[str] = None
    operator_id: Optional[str] = None
    machine_id: Optional[str] = None
    estimated_time: Optional[float] = None
    status: Optional[str] = None

class TaskCreate(TaskBase):
    task_id: str

class Task(TaskBase):
    id: int
    task_id: str
    actual_time: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TelemetryBase(BaseModel):
    machine_id: str
    operator_id: str
    engine_hours: float
    fuel_used: float
    load_cycles: int
    idling_time: float
    seatbelt_status: str
    safety_alert: bool

class TelemetryCreate(TelemetryBase):
    pass

class Telemetry(TelemetryBase):
    id: int
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class TrainingRecommendation(BaseModel):
    title: str
    category: str
    description: str
    duration: int
    reason: str
    priority: str

class PredictionResponse(BaseModel):
    predicted_time: float
    confidence: float
    model_version: str

class AnomalyResponse(BaseModel):
    anomaly: bool
    anomaly_score: float
    reason: Optional[str] = None
