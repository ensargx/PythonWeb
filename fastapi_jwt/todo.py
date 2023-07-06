from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import databases
import sqlalchemy

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./sqlite.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

todos = sqlalchemy.Table(
    "todos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("completed", sqlalchemy.Boolean, default=False),
    sqlalchemy.Column("owner_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)

todo_router = APIRouter()

class TodoIn(BaseModel):
    title: str
    description: str
    owner_id: int
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
async def get_todo_by_id(todo_id):
    query = todos.select().where(todos.c.id == todo_id)
    response = await database.fetch_one(query)
    if not response:
        raise HTTPException(status_code=404, detail="Todo with id {} not found".format(todo_id))
    return response

@todo_router.get("/", response_model=list[Todo])
async def get_todos():
    query = todos.select()
    return await database.fetch_all(query)

@todo_router.post("/", response_model=Todo)
async def create_todo(todo: TodoIn) -> Todo:
    # title or description cannot be empty
    if not todo.title or not todo.description or todo.owner_id is None:
        raise HTTPException(status_code=400, detail=f"Title, Owner or description cannot be empty, {todo}")
    
    query = todos.insert().values(title=todo.title, description=todo.description, completed=False, owner_id=todo.owner_id)
    last_record_id = await database.execute(query)

    return {**todo.dict(), "id": last_record_id, "completed": False}

# put will update only the fields that are passed
@todo_router.put("/{todo_id}")
async def update_todo_by_id(todo_id:int, todo: TodoUpdate | dict):
    todo = dict(todo)
    # check all the values are in the TodoIn model
    if not all(key in TodoUpdate.__fields__ for key in todo.keys()):
        raise HTTPException(status_code=400, detail="Invalid keys passed, {}".format(todo.keys()))

    # only update the fields that are passed with the request body todo
    query = todos.update().where(todos.c.id == todo_id).values(**todo)
    success = await database.execute(query)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {success}

@todo_router.delete("/{todo_id}")
async def delete_todo_by_id(todo_id):
    query = todos.delete().where(todos.c.id == todo_id)
    success = await database.execute(query)
    if not success:
        raise HTTPException(status_code=404, detail="Todo with id {} not found".format(todo_id))
    return {"status": "success", "message": "Todo with id: {} deleted successfully!".format(todo_id)}
