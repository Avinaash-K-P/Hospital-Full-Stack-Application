from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.patient import PatientCreate, PatientUpdate
from app.services.patient_service import (
    create_patient,
    search_patient,
    update_patient,
    delete_patient
)
from app.core.security import require_role

router = APIRouter(prefix="/patient", tags=["Patient"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add Patient
@router.post("/")
def add_patient(patient: PatientCreate, db: Session = Depends(get_db), user=Depends(require_role("doctor"))):
    return create_patient(db, patient)

# 2. Search Patient
@router.get("/search")
def search(query: str, db: Session = Depends(get_db), user=Depends(require_role("doctor"))):
    return search_patient(db, query)

# 3. Update Patient
@router.put("/{patient_id}")
def update(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db), user=Depends(require_role("doctor"))):
    updated = update_patient(db, patient_id, patient)
    if not updated:
        raise HTTPException(status_code=404, detail="Patient not found")
    return updated

# 4. Delete Patient
@router.delete("/{patient_id}")
def delete(patient_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    deleted = delete_patient(db, patient_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}