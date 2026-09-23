import sys
import os
from datetime import datetime

# Add the parent directory of backend to sys.path to allow imports from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import engine, Base, SessionLocal
from app.models.models import Operator, Machine, Task, MachineTelemetry, TrainingModule

def seed_db():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if already seeded
        if db.query(Operator).first():
            print("Database already seeded. Skipping.")
            return

        print("Seeding Operators...")
        operators = [
            Operator(operator_id="OP1001", name="John Doe", skill_level="Expert", safety_score=95.0, efficiency_score=92.0),
            Operator(operator_id="OP1002", name="Jane Smith", skill_level="Intermediate", safety_score=85.0, efficiency_score=88.0),
            Operator(operator_id="OP1003", name="Bob Johnson", skill_level="Beginner", safety_score=75.0, efficiency_score=70.0),
        ]
        db.add_all(operators)

        print("Seeding Machines...")
        machines = [
            Machine(machine_id="EXC001", machine_type="Excavator", machine_age=2, engine_hours=1523.5, status="Active"),
            Machine(machine_id="TRC001", machine_type="Trenching", machine_age=4, engine_hours=3120.0, status="Active"),
            Machine(machine_id="LDR001", machine_type="Loader", machine_age=3, engine_hours=2450.0, status="Maintenance"),
            Machine(machine_id="GRD001", machine_type="Grader", machine_age=5, engine_hours=4200.0, status="Active"),
            Machine(machine_id="DML001", machine_type="Demolition", machine_age=6, engine_hours=5100.0, status="Active"),
        ]
        db.add_all(machines)
        
        db.commit() # Commit to satisfy foreign keys for tasks

        print("Seeding Tasks...")
        tasks = [
            Task(task_id="T001", task_type="Earth Excavation", weather="Sunny", operator_id="OP1001", machine_id="EXC001", estimated_time=60.0, actual_time=58.0, status="Completed"),
            Task(task_id="T002", task_type="Trenching", weather="Rainy", operator_id="OP1002", machine_id="TRC001", estimated_time=45.0, actual_time=52.0, status="Completed"),
            Task(task_id="T003", task_type="Material Loading", weather="Cloudy", operator_id="OP1003", machine_id="LDR001", estimated_time=30.0, actual_time=42.0, status="Completed"),
            Task(task_id="T004", task_type="Grading", weather="Sunny", operator_id="OP1001", machine_id="GRD001", estimated_time=35.0, actual_time=33.0, status="Completed"),
            Task(task_id="T005", task_type="Demolition", weather="Windy", operator_id="OP1002", machine_id="DML001", estimated_time=90.0, actual_time=105.0, status="Completed"),
            Task(task_id="T006", task_type="Earth Excavation", weather="Sunny", operator_id="OP1001", machine_id="EXC001", estimated_time=50.0, status="In Progress"), # Today's task
        ]
        db.add_all(tasks)
        
        print("Seeding Telemetry...")
        telemetry = [
            MachineTelemetry(machine_id="EXC001", operator_id="OP1001", engine_hours=1523.5, fuel_used=5.2, load_cycles=12, idling_time=30.0, seatbelt_status="Fastened", safety_alert=False),
            MachineTelemetry(machine_id="EXC001", operator_id="OP1001", engine_hours=1524.8, fuel_used=3.8, load_cycles=2, idling_time=55.0, seatbelt_status="Unfastened", safety_alert=True),
            MachineTelemetry(machine_id="EXC001", operator_id="OP1001", engine_hours=1526.5, fuel_used=6.1, load_cycles=10, idling_time=15.0, seatbelt_status="Fastened", safety_alert=False),
            MachineTelemetry(machine_id="EXC001", operator_id="OP1001", engine_hours=1530.2, fuel_used=2.0, load_cycles=1, idling_time=60.0, seatbelt_status="Unfastened", safety_alert=True),
        ]
        db.add_all(telemetry)
        
        print("Seeding Training Modules...")
        training_modules = [
            TrainingModule(title="Seatbelt Safety Training", category="Safety", description="Proper seatbelt usage and importance.", duration=15),
            TrainingModule(title="Efficient Machine Operation", category="Efficiency", description="Techniques to reduce idling and save fuel.", duration=30),
            TrainingModule(title="Safe Machine Operation", category="Safety", description="General safety practices and responding to alerts.", duration=45),
            TrainingModule(title="Machine Handling & Safety", category="Operations", description="Handling machine anomalies safely.", duration=60),
        ]
        db.add_all(training_modules)

        db.commit()
        print("Database seeding completed successfully.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
