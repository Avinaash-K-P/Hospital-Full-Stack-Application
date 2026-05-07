from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models.doctor import Doctor
from app.schemas.doctor import DoctorCreate, DoctorUpdate
from app.utils.pagination import paginator
from app.utils.cache import cache_store, CACHE_TTL
import time

#1. Create doctor
def create_doctor(db: Session, doctor: DoctorCreate):
    db_doctor = Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    cache_store.clear() # To clear the Cache
    return db_doctor

#2. List doctor
def list_doctor(db: Session, skip: int = 0, limit: int = 0, sort_by: str = "id", order: str = "asc"):
    query = db.query(Doctor)
    sort_column = getattr(Doctor, sort_by, None)
    if sort_column:
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(asc(sort_column))
    return paginator(query,skip,limit)

#3. Search doctor
def search_doctors(
    db: Session,
    name: str = None,
    specialization: str = None,
):
    cache_key = f"doctors:{name}:{specialization}"
    current_time = time.time()

    if cache_key in cache_store:
        data, timestamp = cache_store[cache_key]

        if current_time - timestamp < CACHE_TTL:
            print("CACHE HIT")
            return data
        else:
            print("Time diff:", current_time - timestamp)  
            print("CACHE EXPIRED")
          
    print("DB HIT")
    
    query = db.query(Doctor)
    if name:
        query = query.filter(Doctor.name.ilike(f"%{name}%"))
    if specialization:
        query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))

    result = query.all()
    cache_store[cache_key] = (result, current_time)
    return result

#4. Update doctor
def update_doctor(db: Session, doctor_id: int, doctor_data: DoctorUpdate):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    for key, value in doctor_data.dict().items():
        setattr(doctor, key, value)
    db.commit()
    db.refresh(doctor)
    return doctor

#5. Delete doctor
def delete_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        return None
    db.delete(doctor)
    db.commit()
    return doctor
