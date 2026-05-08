from sqlalchemy.orm import Session
from app.models.appointment import Appointment
from fastapi import HTTPException
from app.models.doctor import Doctor
from app.models.patient import Patient

# 1. Create appointment

def create_appointment(db, appointment):

    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=400, detail="Doctor not found")

    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient not found")
    appointment_data = appointment.model_dump()

    new_appointment = Appointment(**appointment_data)

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


# 2. Get All appointments
def get_all_appointments(db: Session, skip: int = 0, limit: int = 10):
    query = db.query(Appointment)

    total = query.count()

    data = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": data
    }

# 3. Get by doctor or patient
def get_appointments(db: Session, doctor_id: int = None, patient_id: int = None):
    query = db.query(Appointment)

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)

    return query.all()

# 4. Cancel appointment
def cancel_appointment(db: Session, appointment_id: int):
    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appt:
        return None

    appt.status = "Cancelled"
    db.commit()
    db.refresh(appt)
    return appt

# 5. Notify clients about appointment changes
from app.routes.websocket import connected_clients

async def notify_clients(message: str):
    for client in connected_clients:
        await client.send_text(message)