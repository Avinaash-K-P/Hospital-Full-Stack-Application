from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from app.db.base import Base

class PatientReport(Base):
    __tablename__ = "patient_reports"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    file_name = Column(String(255))
    file_path = Column(String(255))
    filetype = Column(String(50))
    size = Column(Integer)
    uploaded_at = Column(DateTime, default=datetime.utcnow)