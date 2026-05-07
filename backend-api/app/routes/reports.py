from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.services.reports_service import upload_patient_report, get_reports_by_patient, get_report_by_id, log_file_upload
from app.core.security import require_role, get_current_user
from app.utils.constants import ROLES
from app.utils.response import success_response
from fastapi.responses import FileResponse
from fastapi import BackgroundTasks

router = APIRouter(prefix="/report", tags=["Report"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload/{patient_id}")
async def upload_report(
    patient_id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user = Depends(require_role(ROLES[0],ROLES[1]))
):
    content = await file.read()

    data = upload_patient_report(db, patient_id, file, content)

    background_tasks.add_task(log_file_upload, file.filename)

    return success_response(
        message="Report uploaded successfully!",
        data = data
    )

@router.get("/list/{patient_id}")
def list_reports(
    patient_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    data = get_reports_by_patient(db, patient_id, skip, limit)
    return success_response(
        message="Report list fetched!",
        data = data
    )    

@router.get("/download/{report_id}")
def download_report(
    report_id: int, 
    db: Session = Depends(get_db), 
    user=Depends(get_current_user)
):
    data = get_report_by_id(db, report_id)
    return success_response(
    message="Report detail fetched!",
    data = data,
    meta = FileResponse(path= data.file_path,filename= data.file_name)
    )


