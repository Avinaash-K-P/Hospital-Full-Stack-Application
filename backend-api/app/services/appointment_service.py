from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.appointment import Appointment
from fastapi import HTTPException
from app.models.doctor import Doctor
from app.models.patient import Patient
from datetime import timedelta
from app.utils.pagination import paginator
from app.utils.constants import APPOINTMENT_STATUS
from app.utils.time_utils import is_valid_slot, is_within_working_hours

# 1. Create appointment

def create_appointment(db, appointment):

    #Check doctor
    doctor = db.query(Doctor).filter(Doctor.id == appointment.doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=400, detail="Doctor not found")

    #Check patient
    patient = db.query(Patient).filter(Patient.id == appointment.patient_id).first()
    if not patient:
        raise HTTPException(status_code=400, detail="Patient not found")
    
    #Time Slot Check
    slot_start = appointment.appointment_date.replace(second=0, microsecond=0)
    slot_end = slot_start + timedelta(minutes=30)
    if not is_within_working_hours(appointment.appointment_date): 
        raise HTTPException(
            status_code=400,
            detail="Appointments allowed only between 10:00 AM and 6:30 PM"
    )

    # Check 30-minute slots
    if not is_valid_slot(appointment.appointment_date):
        raise HTTPException(
            status_code=400,
            detail="Appointments must be in 30-minute slots (00 or 30 minutes)"
    )

    # To Prevent Double Booking
    existing_doctor = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date >= slot_start,
        Appointment.appointment_date < slot_end
        ).first()
    
    existing_patient = db.query(Appointment).filter(
        Appointment.patient_id == appointment.patient_id,
        Appointment.appointment_date >= slot_start,
        Appointment.appointment_date < slot_end
        ).first()

    print("Incoming:", appointment.appointment_date)

    if existing_doctor:
        raise HTTPException(status_code=400, detail="Time slot already booked")

    if existing_patient:
        raise HTTPException(status_code=400, detail="Patient already has an appointment at this time")

    #create appointment
    new_appointment = Appointment(
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        appointment_date=appointment.appointment_date,
        status="pending"
    )
    print("Creating appointment:", new_appointment)
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment


# 2. Get All appointments
def get_all_appointments(db: Session, skip: int = 0, limit: int = 10, sort_by: str = "id", order: str = "asc"):
    query = db.query(Appointment)
    sort_column = getattr(Appointment, sort_by, None)
    if sort_column:
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
    return paginator(query,skip,limit)

# 3. Get by doctor or patient
def get_appointments(
    db: Session, 
    date: str = None,
    status: str = None,
    user: str = None,
    doctor_id: int = None, 
    patient_id: int = None,
    ):
    query = db.query(Appointment)

    if date:
        query = query.filter(Appointment.appointment_date.like(f"{date}%"))

    if status:
        query = query.filter(Appointment.status == status)

    if doctor_id:
        query = query.filter(Appointment.doctor_id == doctor_id)

    if patient_id:
        query = query.filter(Appointment.patient_id == patient_id)

    return query.all()

# 4. Update appointment
def update_appointments(db: Session, appointment_id: int, status: str):

    if status not in APPOINTMENT_STATUS:
        raise HTTPException(status_code= 400, detail = "Invalid Status")

    appt = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if not appt:
        return None

    appt.status = status
    db.commit()
    db.refresh(appt)
    return appt

# 5. Notify clients about appointment changes
from app.routes.websocket import connected_clients

async def notify_clients(message: str):
    for client in connected_clients:
        await client.send_text(message)