from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.services.doctor_service import (
    create_doctor,
    list_doctor,
    search_doctors,
    update_doctor,
    delete_doctor
)
from app.core.security import require_role, get_current_user
from app.utils.constants import ROLES
from app.utils.response import success_response

router = APIRouter(prefix="/doctor", tags=["Doctor"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add Doctor
@router.post("/")
def add(doctor: DoctorCreate, db: Session = Depends(get_db), user=Depends(require_role(ROLES[0]))):
    data = create_doctor(db, doctor)
    return success_response(
        message = "Doctor added successfully!",
        data =  data 
    )

# 2. List Doctors
@router.get("/list")
def list(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str = "asc",
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = list_doctor(db, skip, limit, sort_by, order)
    return success_response(
        message = "Doctor list fetched!", 
        data = data
    )

# 3. Search by specialization
@router.get("/search")
def search(
    name:str = None,
    specialization: str = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = search_doctors(db, name, specialization)

    return success_response(
        message="Doctor details fetched!",
        data = data
    )

# 4. Update Doctor
@router.put("/update/{doctor_id}")
def update(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db), user=Depends(require_role(ROLES[0]))):
    doctors = update_doctor(db, doctor_id, doctor)
    if not doctors:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return success_response(
        message="Doctor updated successfully!",
        data = doctors
    )

# 5. Delete Doctor
@router.delete("/delete/{doctor_id}")
def delete(doctor_id: int, db: Session = Depends(get_db), user=Depends(require_role(ROLES[0]))):
    data = delete_doctor(db, doctor_id)
    if not data:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return success_response(
        message = "Doctor details deleted!", 
        data = data
    )