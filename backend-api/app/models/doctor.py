from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from app.db.base import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    specialization = Column(String(100))
    is_active = Column(Boolean, default=True)