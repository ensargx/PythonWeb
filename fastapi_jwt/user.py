from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Form, Depends
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from pydantic import BaseModel
from db import database, users
from passlib.context import CryptContext

user_router = APIRouter()

# OAuth2 scheme for authentication will use post data JSON
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login")

JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create user model
class User(BaseModel):
    id: int
    username: str
    name: str
    password: str
    is_active: bool
    todos: list[int] = []

class UserIn(BaseModel):
    username: str
    name: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str

def createToken(data: TokenData):
    return jwt.encode(data, JWT_SECRET_KEY, algorithm="HS256")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

@user_router.post("/register", response_model=dict)
async def register(user: UserIn):

    # check if user already exists
    # if user exists, raise exception
    # else create user
    # return token
    query = users.select().where(users.c.username == user.username)
    status = await database.fetch_one(query)
    if status:
        raise HTTPException(status_code=400, detail="User already exists")
    
    hashed_password = get_password_hash(user.password)
    query = users.insert().values(username=user.username, name=user.name, hashed_password=hashed_password, is_active=True)
    last_record_id = await database.execute(query)
    return {"status": "success", "id": last_record_id}
    

@user_router.post("/login", response_model=Token)
async def login(user: UserLogin):
    # check if user exists
    # if user exists, check password
    # if password matches, return token
    # else raise exception
    # else raise exception
    query = users.select().where(users.c.username == user.username)
    user_data = await database.fetch_one(query)
    if not user_data:
        raise HTTPException(status_code=400, detail="User does not exist")
    
    if not verify_password(user.password, user_data["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    token_data: TokenData = {"username": user.username}
    access_token = createToken(token_data)
    
    return {"access_token": access_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        token_data = TokenData(username=username)
    except:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    query = users.select().where(users.c.username == token_data.username)
    user = await database.fetch_one(query)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

@user_router.get("/me")
async def get_user(): #user: User = Depends(get_current_user)):
    return "Hello"

