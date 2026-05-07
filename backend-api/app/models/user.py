from sqlalchemy import Column, DateTime, Integer, String, Enum
from app.db.base import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    doctor = "doctor"
    patient = "patient"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)   
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)