from fastapi import FastAPI, Depends, Body
from datetime import datetime, timedelta
from typing import Annotated
from auth import router, oauth2_scheme

app = FastAPI()

# /auth router
app.include_router(router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/protected")
async def protected(data: dict = Body(), token: str = Depends(oauth2_scheme)):
    print(data)
    print(token)
    return {"message": "Authorized"}
