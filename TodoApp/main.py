from fastapi import FastAPI, Depends, Path
import models
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from models import Todo
from fastapi.exceptions import HTTPException
from starlette import status
from pydantic import BaseModel, Field


app = FastAPI()

#Create the database tables
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str=Field(min_length=3, max_length=75)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(ge=1, le=5)
    complete: bool 



#Read all todo items
@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todo).all()


#Read a single todo item by id - With status code and Path parameter validation
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK) 

async def read_todo(db: db_dependency, todo_id: int =Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo item not found")

#Create a new todo item

@app.post("/todo", status_code=status.HTTP_201_CREATED)

async def create_todo(todo_request : TodoRequest, db: db_dependency):

    todo_model = Todo(
       **todo_request.model_dump()
    )
    db.add(todo_model)
    db.commit()
