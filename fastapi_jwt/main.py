from fastapi import FastAPI, Depends, Body
from datetime import datetime, timedelta
from typing import Annotated
from auth import router, oauth2_scheme, convert_jwt

app = FastAPI()

# /auth router
app.include_router(router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/protected")
async def protected(data: dict = Body(), data_user: dict = Depends(convert_jwt)):
    
    return {"data": data, "data_user": data_user}
    
    json_data = {"data": data, "token": token, "message": f"Welcome to the protected route, {username}"}
    return json_data
