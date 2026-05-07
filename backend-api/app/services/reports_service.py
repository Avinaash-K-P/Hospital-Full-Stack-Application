import os
import uuid
from fastapi import HTTPException
from app.models.reports import PatientReport
from app.utils.pagination import paginator

UPLOAD_DIR = "uploads"
ALLOWED_TYPES = ["application/pdf", "image/png", "image/jpeg"]
MAX_SIZE = 2 * 1024 * 1024  # 2MB


def upload_patient_report(db, patient_id: int, file, content: bytes):

    #  Validate type
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    #  Validate size
    if len(content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File too large")

    #  Create upload folder
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    #  Unique filename
    unique_name = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_name)

    #  Save file
    with open(file_path, "wb") as buffer:
        buffer.write(content)

    #  Save metadata in DB
    new_report = PatientReport(
        patient_id=patient_id,
        file_name=unique_name,
        file_path=file_path,
        filetype=file.content_type,
        size=len(content)
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report

def get_reports_by_patient(db, patient_id: int, skip: int = 0, limit: int = 10):
    
    query = db.query(PatientReport).filter(
        PatientReport.patient_id == patient_id
    )
    return paginator(query,skip,limit)

def get_report_by_id(db, report_id: int):
    report = db.query(PatientReport).filter(
        PatientReport.id == report_id
    ).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    return report

def log_file_upload(filename: str):
    with open("upload_log.txt", "a") as f:
        f.write(f"{filename} uploaded\n")