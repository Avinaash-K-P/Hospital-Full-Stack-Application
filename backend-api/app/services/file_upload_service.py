import os
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from app.models.file_upload import FileUpload

UPLOAD_DIR = "uploads"


def save_file_to_disk(file: UploadFile):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_location = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())

    return file_location


def upload_file_service(db: Session, patient_id: int, file: UploadFile):

    file_path = save_file_to_disk(file)

    db_file = FileUpload(
        patient_id=patient_id,
        file_name=file.filename,
        file_path=file_path,
        file_type=file.content_type
    )

    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return db_file