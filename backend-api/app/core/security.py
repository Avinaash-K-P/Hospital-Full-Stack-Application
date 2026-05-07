from passlib.context import CryptContext
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.session import SessionLocal
from app.models.user import User

security = HTTPBearer(auto_error=True)

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("TOKEN PAYLOAD:", payload)   
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        db.close()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_role(*roles):
    def role_checker(user=Depends(get_current_user)):
        if user.role not in roles and user.role != "admin":
            raise HTTPException(status_code=403, detail="Access forbidden")
        return user
    return role_checker    