import pytest
from fastapi.testclient import TestClient

from app.api.dependencies.database import get_db
from app.main import app


@pytest.fixture
def database():
    return {"users": {}}


@pytest.fixture
def user():
    return {"id": 1, "name": "Ana", "password": "secret", "roles": ["reader"]}


@pytest.fixture
def client(database):
    app.dependency_overrides[get_db] = lambda: database
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
