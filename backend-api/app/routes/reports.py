from fastapi import APIRouter, UploadFile, File, Depends
import shutil
import os
from fastapi.responses import FileResponse

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/upload/{patient_id}",  tags=["Reports"])
async def upload_report(patient_id: int, file: UploadFile = File(...)):
    file_path = f"{UPLOAD_DIR}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "file_name": file.filename,
        "file_path": file_path
    }



@router.get("/download/{filename}", tags=["Reports"])
def download_file(filename: str):
    file_path = f"uploads/{filename}"
    return FileResponse(file_path, media_type="application/octet-stream", filename=filename)
