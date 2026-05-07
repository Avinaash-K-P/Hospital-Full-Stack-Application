from pydantic import BaseModel
from datetime import datetime

class FileUpload(BaseModel):
    id: int
    patient_id: int
    file_name: str
    file_path: str
    file_type: str
    size: int
    uploaded_at: datetime

    class Config:
        from_attributes = True