from database import engine
from fastapi import FastAPI
from routers import auth, todos, admin, users
import models



app = FastAPI()

#Create the database tables
models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

