from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.services.doctor_service import (
    create_doctor,
    search_doctors,
    update_doctor,
    delete_doctor
)
from app.core.security import get_current_user, require_role

router = APIRouter(prefix="/doctor", tags=["Doctor"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Add Doctor
@router.post("/")
def add_doctor(doctor: DoctorCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_doctor(db, doctor)

# 2. Search by specialization
@router.get("/search")
def search(
    specialization: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return search_doctors(db, specialization, skip, limit)


# 3. Update Doctor
@router.put("/{doctor_id}")
def update(doctor_id: int, doctor: DoctorUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    updated = update_doctor(db, doctor_id, doctor)
    if not updated:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return updated

# 4. Delete Doctor
@router.delete("/{doctor_id}")
def delete(doctor_id: int, db: Session = Depends(get_db), user=Depends(require_role("admin"))):
    deleted = delete_doctor(db, doctor_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return {"message": "Doctor deleted successfully"}