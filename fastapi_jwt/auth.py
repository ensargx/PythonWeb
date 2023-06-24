from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Form
from datetime import datetime, timedelta
from fastapi import HTTPException, status

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

def createToken(data: dict):
    return jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")

@router.post("/register")
def register(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(minutes=30)
    return createToken(data)

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    """
    only for admin
    """
    if username == "admin" and password == "admin":
        data = {
            "username": username,
            "password": password,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        return createToken(data)
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )