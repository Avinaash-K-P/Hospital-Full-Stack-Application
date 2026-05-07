from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AppointmentCreate(BaseModel):
    doctor_id: int
    patient_id: int
    appointment_date: datetime

class AppointmentUpdate(BaseModel):
    status: Optional[str] = None