from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import databases
import sqlalchemy

# SQLAlchemy specific code, as with any other app
DATABASE_URL = "sqlite:///./todos.db"
# DATABASE_URL = "postgresql://user:password@postgresserver/db"

database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

todos = sqlalchemy.Table(
    "todos",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String),
    sqlalchemy.Column("description", sqlalchemy.String),
)

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


todo_router = APIRouter()

class TodoIn(BaseModel):
    title: str
    description: str

class Todo(BaseModel):
    id: int
    title: str
    description: str


@todo_router.on_event("startup")
async def startup():
    await database.connect()

@todo_router.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@todo_router.get("/{todo_id}", response_model=Todo)
async def get_todo_by_id(todo_id):
    pass

@todo_router.get("s/", response_model=list[Todo])
async def get_todos():
    query = todos.select()
    return await database.fetch_all(query)

@todo_router.post("/", response_model=Todo)
async def create_todo(todo: TodoIn) -> Todo:
    query = todos.insert().values(title=todo.title, description=todo.description)
    last_record_id = await database.execute(query)
    return {**todo.dict(), "id": last_record_id}

@todo_router.put("/{todo_id}", response_model=Todo)
async def update_todo_by_id(todo_id:int, todo: TodoIn):
    query = todos.update().where(todos.c.id == todo_id).values(title=todo.title, description=todo.description)
    success = await database.execute(query)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {**todo.dict(), "id": todo_id}

@todo_router.delete("/{todo_id}")
async def delete_todo_by_id(todo_id):
    query = todos.delete().where(todos.c.id == todo_id)
    success = await database.execute(query)
    if not success:
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"message": "Todo with id: {} deleted successfully!".format(todo_id)}
