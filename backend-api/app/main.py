from fastapi import FastAPI, Request, HTTPException
from app.db.base import Base
from app.db.session import engine
from app.routes import auth, doctor, patient, appointment, reports, websocket
from fastapi.middleware.cors import CORSMiddleware 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.response import error_response

app = FastAPI(
    title="Hospital Management API",
    description="Advanced Hospital Backend and feature Engineering using FastAPI",
    version="4.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(reports.router)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"message": "API is running successfully!"}

# Global Exception Handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):

    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.detail)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):

    formatted_errors = []

    for err in exc.errors():
        formatted_errors.append({
            "field": err["loc"][-1],
            "message": err["msg"]
        })

    return JSONResponse(
        status_code=422,
        content=error_response(
            message="Validation failed",
            errors=formatted_errors
        )
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):

    print("UNEXPECTED ERROR:", exc)

    return JSONResponse(
        status_code=500,
        content=error_response("Internal Server Error")
    )