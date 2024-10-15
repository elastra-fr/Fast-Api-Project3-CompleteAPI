from database import SessionLocal
from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from models import Todo
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from typing import Annotated
from .auth import get_current_user

 



router = APIRouter(
      prefix="/admin",
    tags=["admin"]
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/todo", status_code=status.HTTP_200_OK)

async def read_all(user: user_dependency, db: db_dependency):
    
        if user is None or user.get("role") != "admin":
            raise HTTPException(status_code=401, detail="User not authenticated")
    
        return db.query(Todo).all()
