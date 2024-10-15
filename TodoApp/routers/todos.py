from database import SessionLocal
from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from models import Todo
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated

 



router = APIRouter()



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
@router.get("/")
async def read_all(db: db_dependency):
    return db.query(Todo).all()


#Read a single todo item by id - With status code and Path parameter validation
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK) 

async def read_todo(db: db_dependency, todo_id: int =Path(gt=0)):
    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo item not found")

#Create a new todo item

@router.post("/todo", status_code=status.HTTP_201_CREATED)

async def create_todo(todo_request : TodoRequest, db: db_dependency):

    todo_model = Todo(
       **todo_request.model_dump()
    )
    db.add(todo_model)
    db.commit()

#Update a todo item by id - With status code and Path parameter validation

@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)

async def update_todo(todo_request: TodoRequest, db: db_dependency, todo_id: int = Path(gt=0)):

    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete
    
    db.add(todo_model)
    db.commit()

#Delete a todo item by id - With status code and Path parameter validation

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)

async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):

    todo_model = db.query(Todo).filter(Todo.id == todo_id).first()

    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    db.delete(todo_model)
    db.commit()

