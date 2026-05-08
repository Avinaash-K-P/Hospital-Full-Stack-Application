from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.routes import auth, doctor, patient, appointment, reports, websocket
from fastapi.middleware.cors import CORSMiddleware 

app = FastAPI(title="Hospital Management API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(reports.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"message": "API is running "}