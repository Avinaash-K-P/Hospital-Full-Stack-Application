from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate
from app.utils.pagination import paginator

# 1. Add Patient
def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

#2. List Patient
def list_patient(db: Session, skip: int = 0,limit: int = 10, sort_by: str = id, order = "asc"):
    query = db.query(Patient)
    sort_column = getattr(Patient, sort_by, None)
    if sort_column:
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
    return paginator(query,skip,limit)

# Search by name or phone
def search_patient(
        db: Session, 
        name:str=None,
        phone:str=None
        ):   
    query = db.query(Patient)
    if name:
        query = query.filter(Patient.name.ilike(f"%{name}%"))
    if phone:
        query = query.filter(Patient.phone.ilike(f"%{phone}%"))     
    return query.all()

# 3. Update Patient
def update_patient(db: Session, patient_id: int, patient: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        return None

    for key, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient

# 4. Delete Patient
def delete_patient(db: Session, patient_id: int):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        return None

    db.delete(db_patient)
    db.commit()
    return db_patient