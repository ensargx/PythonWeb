from fastapi import FastAPI, Depends, Body
from user import user_router, oauth2_scheme
from todo import todo_router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

# /user router
app.include_router(user_router, prefix="/user")

# /todo router, it is protected by oauth2_scheme, requires logged in user
app.include_router(todo_router, prefix="/todo")

@app.get("/")
async def root():
    return {"message": "Hello World"}
