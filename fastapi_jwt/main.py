from fastapi import FastAPI, Depends, Body
from datetime import datetime, timedelta
from typing import Annotated
from auth import auth_router, oauth2_scheme, convert_jwt
from todo import todo_router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)



# /auth router
app.include_router(auth_router, prefix="/auth")

# /user router
app.include_router(todo_router, prefix="/todo")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/protected")
async def protected(data: dict = Body(), data_user: dict = Depends(convert_jwt)):
    
    return {"data": data, "data_user": data_user}
    
    json_data = {"data": data, "token": token, "message": f"Welcome to the protected route, {username}"}
    return json_data
