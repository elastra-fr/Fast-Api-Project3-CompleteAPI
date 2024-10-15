from database import engine
from fastapi import FastAPI
import models
from routers import auth, todos



app = FastAPI()

#Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)

