from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models
from app.schemas import schemas

router = APIRouter(
    prefix="/api/operators",
    tags=["operators"]
)

@router.get("", response_model=List[schemas.Operator])
@router.get("/", response_model=List[schemas.Operator], include_in_schema=False)
def get_operators(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operators = db.query(models.Operator).offset(skip).limit(limit).all()
    return operators

@router.get("/{operator_id}", response_model=schemas.Operator)
def get_operator(operator_id: str, db: Session = Depends(get_db)):
    operator = db.query(models.Operator).filter(models.Operator.operator_id == operator_id).first()
    if operator is None:
        raise HTTPException(status_code=404, detail="Operator not found")
    return operator
