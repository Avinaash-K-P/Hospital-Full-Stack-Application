from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    name: str
    phone: str
    age: int

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None