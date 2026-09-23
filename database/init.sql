-- init.sql
-- Database Schema for Smart Operator Assistant

CREATE TABLE IF NOT EXISTS operators (
    id SERIAL PRIMARY KEY,
    operator_id VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    skill_level VARCHAR(50),
    safety_score FLOAT DEFAULT 100.0,
    efficiency_score FLOAT DEFAULT 100.0
);

CREATE TABLE IF NOT EXISTS machines (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50) UNIQUE NOT NULL,
    machine_type VARCHAR(100) NOT NULL,
    machine_age INT,
    engine_hours FLOAT,
    status VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(50) UNIQUE NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    weather VARCHAR(50),
    operator_id VARCHAR(50) REFERENCES operators(operator_id),
    machine_id VARCHAR(50) REFERENCES machines(machine_id),
    estimated_time FLOAT,
    actual_time FLOAT,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS machine_telemetry (
    id SERIAL PRIMARY KEY,
    machine_id VARCHAR(50) REFERENCES machines(machine_id),
    operator_id VARCHAR(50) REFERENCES operators(operator_id),
    engine_hours FLOAT,
    fuel_used FLOAT,
    load_cycles INT,
    idling_time FLOAT,
    seatbelt_status VARCHAR(50),
    safety_alert BOOLEAN,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS safety_events (
    id SERIAL PRIMARY KEY,
    operator_id VARCHAR(50) REFERENCES operators(operator_id),
    machine_id VARCHAR(50) REFERENCES machines(machine_id),
    event_type VARCHAR(100),
    severity VARCHAR(50),
    description TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(50) REFERENCES tasks(task_id),
    predicted_time FLOAT,
    confidence FLOAT,
    model_version VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS training_modules (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    category VARCHAR(100),
    description TEXT,
    duration INT
);

CREATE TABLE IF NOT EXISTS operator_training (
    id SERIAL PRIMARY KEY,
    operator_id VARCHAR(50) REFERENCES operators(operator_id),
    training_id INT REFERENCES training_modules(id),
    status VARCHAR(50) DEFAULT 'Recommended',
    completion_date TIMESTAMP
);
