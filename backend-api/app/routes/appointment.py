from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.appointment import AppointmentCreate
from app.services.appointment_service import (
    create_appointment,
    get_all_appointments,
    get_appointments,
    cancel_appointment
)
from app.core.security import get_current_user

router = APIRouter(prefix="/appointment", tags=["Appointment"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Create Appointment 
@router.post("/")
def create(appointment: AppointmentCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_appointment(db, appointment)

# 2. Get all appointments
@router.get("/")
def all_appointments(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_all_appointments(db, skip, limit)

# 3. Get by doctor or patient
@router.get("/filter")
def filter_appointments(
    doctor_id: int = None,
    patient_id: int = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    return get_appointments(db, doctor_id, patient_id)

# 3. Cancel appointment
@router.put("/cancel/{appointment_id}")
def cancel(appointment_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    appt = cancel_appointment(db, appointment_id)

    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    return {"message": "Appointment cancelled successfully"}