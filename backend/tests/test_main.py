import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from app.main import app, is_even


@pytest.fixture
def client():
    return TestClient(app)


def test_root_http(client):
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Laboratório distribuído funcionando!"}


@pytest.mark.parametrize(
    ("number", "expected"),
    [
        (1, False),
        (2, True),
        (3, False),
        (4, True),
        (5, False),
        (6, True),
    ],
)
def test_is_even_http(number, expected, client):
    response = client.get(f"/is-even/{number}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"result": expected}


@pytest.mark.parametrize(
    "param",
    ["a", 2.3],
)
def test_is_even_http_with_invalid_params(client, param):
    response = client.get(f"/is-even/{param}")
    msg = response.json()["detail"][0]["msg"]

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert (
        msg == "Input should be a valid integer, unable to parse string as an integer"
    )


def test_is_even_func_with_str_param():
    with pytest.raises(HTTPException):
        is_even("a")


def test_is_even_func_with_float_param():
    with pytest.raises(HTTPException):
        is_even(1.2)
