from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Operator(Base):
    __tablename__ = "operators"
    
    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    skill_level = Column(String)
    safety_score = Column(Float, default=100.0)
    efficiency_score = Column(Float, default=100.0)


class Machine(Base):
    __tablename__ = "machines"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, unique=True, index=True, nullable=False)
    machine_type = Column(String, nullable=False)
    machine_age = Column(Integer)
    engine_hours = Column(Float)
    status = Column(String)


class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True, nullable=False)
    task_type = Column(String, nullable=False)
    weather = Column(String)
    operator_id = Column(String, ForeignKey("operators.operator_id"))
    machine_id = Column(String, ForeignKey("machines.machine_id"))
    estimated_time = Column(Float)
    actual_time = Column(Float)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MachineTelemetry(Base):
    __tablename__ = "machine_telemetry"
    
    id = Column(Integer, primary_key=True, index=True)
    machine_id = Column(String, ForeignKey("machines.machine_id"))
    operator_id = Column(String, ForeignKey("operators.operator_id"))
    engine_hours = Column(Float)
    fuel_used = Column(Float)
    load_cycles = Column(Integer)
    idling_time = Column(Float)
    seatbelt_status = Column(String)
    safety_alert = Column(Boolean)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class SafetyEvent(Base):
    __tablename__ = "safety_events"
    
    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(String, ForeignKey("operators.operator_id"))
    machine_id = Column(String, ForeignKey("machines.machine_id"))
    event_type = Column(String)
    severity = Column(String)
    description = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("tasks.task_id"))
    predicted_time = Column(Float)
    confidence = Column(Float)
    model_version = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TrainingModule(Base):
    __tablename__ = "training_modules"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    category = Column(String)
    description = Column(String)
    duration = Column(Integer)


class OperatorTraining(Base):
    __tablename__ = "operator_training"
    
    id = Column(Integer, primary_key=True, index=True)
    operator_id = Column(String, ForeignKey("operators.operator_id"))
    training_id = Column(Integer, ForeignKey("training_modules.id"))
    status = Column(String, default="Recommended")
    completion_date = Column(DateTime(timezone=True), nullable=True)
