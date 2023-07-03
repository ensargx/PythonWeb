from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Form, Depends
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from pydantic import BaseModel

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", )

JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

# Create user model
class User(BaseModel):
    username: str
    password: str

def createToken(data: dict):
    return jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")

@router.post("/register", response_model=str)
def register(user: User):

    data = {"username": user["username"]}
    data["exp"] = datetime.utcnow() + timedelta(minutes=30)

    return createToken(data)

@router.post("/login")
def login(user: User):
    """
    only for admin
    """
    if user["username"] == "admin" and user["password"] == "admin":
        data = {
            "username": user["username"],
            "password": user["password"],
            "exp": datetime.utcnow() + timedelta(minutes=30)
        }
        return {"access_token" : createToken(data)}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )

def convert_jwt(token: str = Depends(oauth2_scheme)):
    try:
        # decode token and return the data inside the token
        return jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
    except:
        raise HTTPException(401, "Invalid token or expired token")
    