from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import database, todos
from fastapi import Depends
from user import JWTBearer, TokenData

todo_router = APIRouter()

class TodoIn(BaseModel):
    title: str
    description: str
    completed: bool = False

class Todo(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int

class TodoUpdate(BaseModel):
    title: str
    description: str
    completed: bool

@todo_router.on_event("startup")
async def startup():
    await database.connect()

@todo_router.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@todo_router.get("/{todo_id}", response_model=Todo)
async def get_todo_by_id(todo_id : int, user: TokenData = Depends(JWTBearer())):
    query = todos.select().where(todos.c.id == todo_id, todos.c.owner_id == user["id"])
    response = await database.fetch_one(query)
    if not response:
        raise HTTPException(status_code=404, detail="Todo with id {} not found".format(todo_id))
    return response

@todo_router.get("/", response_model=list[Todo])
async def get_todos(user: TokenData = Depends(JWTBearer())):
    query = todos.select().where(todos.c.owner_id == user["id"])
    return await database.fetch_all(query)

@todo_router.post("/", response_model=Todo)
async def create_todo(todo: TodoIn, user: TokenData = Depends(JWTBearer())) -> Todo:
    # title or description cannot be empty
    if not todo.title or not todo.description:
        raise HTTPException(status_code=400, detail=f"Title or description cannot be empty, {todo}")
    
    query = todos.insert().values(title=todo.title, description=todo.description, completed=False, owner_id=user["id"])
    last_record_id = await database.execute(query)

    return {**todo.dict(), "id": last_record_id, "completed": False, "owner_id": user["id"]}

# put will update only the fields that are passed
@todo_router.put("/{todo_id}")
async def update_todo_by_id(todo_id:int, todo: TodoUpdate | dict, user: TokenData = Depends(JWTBearer())):
    todo = dict(todo)
    # check all the values are in the TodoIn model
    if not all(key in TodoUpdate.__fields__ for key in todo.keys()):
        raise HTTPException(status_code=400, detail="Invalid keys passed, {}".format(todo.keys()))

    # only update the fields that are passed with the request body todo
    query = todos.update().where(todos.c.id == todo_id, todos.c.owner_id == user["id"]).values(**todo)
    success = await database.execute(query)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {success}

@todo_router.delete("/{todo_id}")
async def delete_todo_by_id(todo_id, user: TokenData = Depends(JWTBearer())):
    query = todos.delete().where(todos.c.id == todo_id, todos.c.owner_id == user["id"])
    success = await database.execute(query)
    if not success:
        raise HTTPException(status_code=404, detail="Todo with id {} not found".format(todo_id))
    return {"status": "success", "message": "Todo with id: {} deleted successfully!".format(todo_id)}
    