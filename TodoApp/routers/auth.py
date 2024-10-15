from fastapi import APIRouter, Depends
from pydantic import BaseModel 
from models import Users
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal
from typing import Annotated
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CreateUserRequest(BaseModel):
    username: str
    email : str
    first_name: str
    last_name: str
    password: str
    role: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#Authenticate a user
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    
    #Check if the user exists
    if not user:
        return False
    
    #Check if the password is correct
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    #Return the user if the user exists and the password is correct
    return user


#Create a new user

@router.post("/auth/", status_code=status.HTTP_201_CREATED) 

async def create_user(db:db_dependency ,create_user_request: CreateUserRequest):
    create_user_model = Users(
        username = create_user_request.username,
        email = create_user_request.email,
        first_name = create_user_request.first_name,
        last_name = create_user_request.last_name,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        role = create_user_request.role,
        is_active = True
    )

    db.add(create_user_model)
    db.commit()

@router.post("/token")

async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):   
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return {"error": "Incorrect username or password"}
    
    return {"Success": "Login Successful"}








    

