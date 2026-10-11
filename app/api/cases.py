from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse

router = APIRouter(prefix="/cases", tags=["Cases"])

from sqlalchemy import func

@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(case_in: CaseCreate, db: Session = Depends(get_db)):
    """Create a new missing person investigation case."""
    clean_number = case_in.case_number.strip()
    existing = db.query(Case).filter(func.lower(Case.case_number) == clean_number.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Case with number '{clean_number}' already exists. Please use a different case code."
        )

    case_data = case_in.model_dump()
    case_data["case_number"] = clean_number
    case = Case(**case_data)
    db.add(case)
    db.commit()
    db.refresh(case)
    return case

@router.get("", response_model=List[CaseResponse])
def list_cases(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all cases."""
    return db.query(Case).offset(skip).limit(limit).all()

@router.get("/{id}", response_model=CaseResponse)
def get_case(id: int, db: Session = Depends(get_db)):
    """Get case by ID."""
    case = db.query(Case).filter(Case.id == id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")
    return case

@router.put("/{id}", response_model=CaseResponse)
def update_case(id: int, case_in: CaseUpdate, db: Session = Depends(get_db)):
    """Update case details."""
    case = db.query(Case).filter(Case.id == id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    update_data = case_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)

    db.commit()
    db.refresh(case)
    return case

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_case(id: int, db: Session = Depends(get_db)):
    """Delete a case."""
    case = db.query(Case).filter(Case.id == id).first()
    if not case:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Case not found.")

    db.delete(case)
    db.commit()
    return None
