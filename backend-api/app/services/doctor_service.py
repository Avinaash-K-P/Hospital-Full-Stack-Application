from sqlalchemy.orm import Session
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate

def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def search_doctors(db: Session, specialization: str, skip: int = 0, limit: int = 10):
    query = db.query(Doctor).filter(
        Doctor.specialization.ilike(f"%{specialization}%")
    )

    total = query.count()

    doctors = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": doctors
    }

def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorUpdate):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    for key, value in doctor_data.dict().items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

def delete_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    db.delete(doctor)
    db.commit()
    return doctor
