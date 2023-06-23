from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/register")
async def register(username: str, password: str):
    """
    Creates and returns JWT token for user with username and exp. time 1 mounth
    """
    