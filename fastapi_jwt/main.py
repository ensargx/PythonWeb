from fastapi import FastAPI, Depends, Body
from datetime import datetime, timedelta
import auth
from typing import Annotated

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
async def register(username: str, password: str):
    """
    Creates and returns JWT token for user with username and exp. time 1 mounth
    """
    # Create JWT token for user with username and exp. time 1 mounth
    data = {"username": username, "exp": datetime.utcnow() + timedelta(days=30)}
    #token = createToken(data)

    print(username, password)

    token = auth.createToken(data)
    return {"token": token}

    # Say client to set header "Authentication: Bearer <token>"


@app.post("/protected")
async def protected(token: Annotated[str, Depends(auth.login_required)],data: str = Body()):
    print(data)
    print(token)
    return {"message": "Authorized"}
