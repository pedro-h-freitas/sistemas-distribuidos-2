import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.core.config import TEST_DATABASE_URL
from app.database.base import Base
from app.main import app
from app.models import User


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def database(test_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(
        bind=connection,
        join_transaction_mode="create_savepoint",
    )
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def user():
    return User(id=1, name="Ana", password="secret", roles=["reader"])


@pytest.fixture
def user_data():
    return {"id": 1, "name": "Ana", "password": "secret", "roles": ["reader"]}


@pytest.fixture
def client(database):
    app.dependency_overrides[get_db] = lambda: database
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
