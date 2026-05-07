from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.patient import PatientCreate, PatientUpdate
from app.services.patient_service import (
    create_patient,
    list_patient,
    search_patient,
    update_patient,
    delete_patient
)
from app.core.security import require_role, get_current_user
from app.utils.constants import ROLES
from app.utils.response import success_response

router = APIRouter(prefix="/patient", tags=["Patient"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add Patient
@router.post("/")
def add(patient: PatientCreate, db: Session = Depends(get_db), user=Depends(require_role(ROLES[0]))):
    data = create_patient(db, patient)
    return success_response(
        message="Patient added successfully!",
        data = data
    )

# 2. List Patient

@router.get("/list")
def list(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str ="asc",
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = list_patient(db, skip, limit, sort_by, order)
    return success_response(
        message="Patient list fetched!",
        data = data
    )    

# 2. Search Patient
@router.get("/search")
def search(
    name:str=None, 
    phone:str=None, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
    ):
    data = search_patient(db, name, phone)
    return success_response(
        message="Patient details fetched!",
        data = data
    )    

# 3. Update Patient
@router.put("/update/{patient_id}")
def update(patient_id: int, patient: PatientUpdate, db: Session = Depends(get_db), user=Depends(require_role(ROLES[0]))):
    data = update_patient(db, patient_id, patient)
    if not data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return success_response(
        message="Patient details updated!",
        data = data
    )    

# 4. Delete Patient
@router.delete("/delete/{patient_id}")
def delete(patient_id: int, db: Session = Depends(get_db), user=Depends(require_role(ROLES[0]))):
    data = delete_patient(db, patient_id)
    if not data:
        raise HTTPException(status_code=404, detail="Patient not found")
    return success_response(
        message="Patient details deleted!",
        data = data
    )    