from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from datetime import datetime
from app.db.base import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="Scheduled")