from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.appointment import AppointmentCreate
from app.services.appointment_service import(
    create_appointment,
    get_all_appointments,
    get_appointments,
    update_appointments,
)
from app.core.security import require_role, get_current_user
from app.utils.constants import ROLES
from app.utils.background_tasks import notify_doctor
from app.utils.response import success_response

router = APIRouter(prefix="/appointment", tags=["Appointment"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Create Appointment 
@router.post("/")
def add_appointments(
    appointment: AppointmentCreate, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db), 
    user=Depends(require_role(ROLES[2]))):

    data = create_appointment(db, appointment)
    
    background_tasks.add_task(
        notify_doctor,
        appointment.doctor_id
    )
    return success_response(
        message="Appointment booked successfully!",
        data = data
    )

# 2. Get all appointments
@router.get("/")
def all_appointments(
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "id",
    order: str ="asc",
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = get_all_appointments(db, skip, limit, sort_by, order)
    return success_response(
        message="Appointment list fetched!",
        data = data
    )

# 3. Get by doctor or patient
@router.get("/")
def filter_appointments(
    date: str = None,
    status: str = None,
    doctor_id: int = None,
    patient_id: int = None,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    data = get_appointments(db, date, status, user, doctor_id, patient_id)   
    return success_response(
        message="Appointment detail fetched!",
        data = data
    )

@router.put("/{appointment_id}/")
def update_status(
    appointment_id: int,
    status: str,
    db: Session = Depends(get_db),
    user=Depends(require_role(ROLES[0],ROLES[1]))
):
    data = update_appointments(db, appointment_id, status)

    if not data:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    return success_response(
        message="Appointment details updated!",
        data = data
    )
