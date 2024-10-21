from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from ..database import Base
from ..main import app
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
import pytest
from ..models import Todo, Users
from ..routers.auth import bcrypt_context


SQLALCHEMY_DATABASE_URL = 'sqlite:///testdb.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL
                        , connect_args={'check_same_thread': False},
                        poolclass=StaticPool) 

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

Base.metadata.create_all(bind=engine)   

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "testuser", 
            "id": 1,
            'role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo= Todo(
        title="Test Todo",
        description="Test Description",
        priority=1,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit() 


@pytest.fixture
def test_user():
    user = Users(
        email="test@test.com",
        username="testuser",
        first_name="Test",
        last_name="User",
        hashed_password=bcrypt_context.hash("password"),
        role="admin"

    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
