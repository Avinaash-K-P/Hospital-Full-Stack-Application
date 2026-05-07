from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.schemas.user import ForgotPasswordRequest, ResetPasswordRequest, UserCreate, UserLogin
from app.services.auth_service import create_user, get_user_by_email
from app.models.user import User 
from app.core.security import hash_password, verify_password, create_access_token
from app.utils.response import success_response 
from datetime import datetime, timedelta, UTC
from app.utils.token import generate_reset_token

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    data = create_user(db, user)
    return success_response(
        message="User added succesfully!",
        data = data
    )

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role,
        "sub": db_user.email  
    })

    return success_response(
        message = "User login successful!",
        data = { 
            "access_token": token,
            "token_type": "bearer" 
            }
    )

@router.post("/forgot-password")
def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_reset_token()

    user.reset_token = token
    user.reset_token_expiry = datetime.now(UTC) + timedelta(minutes=15)

    db.commit()

    return success_response(
        "Password reset token generated",
        {
            "reset_token": token
        }
    )

@router.post("/reset-password")
def reset_password(
    request: ResetPasswordRequest,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.reset_token == request.token
    ).first()

    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")

    if datetime.utcnow() > user.reset_token_expiry:
        raise HTTPException(status_code=400, detail="Token expired")

    user.password = hash_password(request.new_password)

    user.reset_token = None
    user.reset_token_expiry = None

    db.commit()

    return success_response(
        "Password reset successful"
    )