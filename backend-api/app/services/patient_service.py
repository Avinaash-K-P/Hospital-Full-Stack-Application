from sqlalchemy.orm import Session
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate

# 1. Add Patient
def create_patient(db: Session, patient: PatientCreate):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

# 2. Search by name or phone
def search_patient(db: Session, query: str):
    return db.query(Patient).filter(
        (Patient.name.ilike(f"%{query}%")) |
        (Patient.phone.ilike(f"%{query}%"))
    ).all()

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