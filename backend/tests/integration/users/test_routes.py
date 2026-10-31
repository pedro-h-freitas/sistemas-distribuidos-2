import pytest


def test_create_and_list_users(client, user_data):
    created = client.post("/users", json=user_data)

    assert created.status_code == 201
    assert created.json() == user_data
    listed = client.get("/users")
    assert listed.status_code == 200
    assert listed.json() == [user_data]


def test_get_user(client, user_data):
    client.post("/users", json=user_data)

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json() == user_data


def test_get_missing_user_returns_404(client):
    response = client.get("/users/9")

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


def test_duplicate_user_returns_409_and_keeps_original(client, user_data):
    client.post("/users", json=user_data)

    response = client.post("/users", json={**user_data, "name": "Bia"})

    assert response.status_code == 409
    assert client.get("/users/1").json() == user_data


def test_update_roles(client, user_data):
    client.post("/users", json=user_data)

    response = client.put("/users/1/roles", json=["admin", "reader"])

    expected = {**user_data, "roles": ["admin", "reader"]}
    assert response.status_code == 200
    assert response.json() == expected
    assert client.get("/users/1").json() == expected


def test_patch_user_preserves_unset_fields(client, user_data):
    client.post("/users", json=user_data)

    response = client.patch("/users/1", json={"name": "Bia"})

    expected = {**user_data, "name": "Bia"}
    assert response.status_code == 200
    assert response.json() == expected
    assert client.get("/users/1").json() == expected


def test_delete_user(client, user_data):
    client.post("/users", json=user_data)

    response = client.delete("/users/1")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get("/users/1").status_code == 404
    assert client.get("/users").json() == []


@pytest.mark.parametrize(
    "method,path,json",
    [
        ("put", "/users/9/roles", ["admin"]),
        ("patch", "/users/9", {"name": "Bia"}),
        ("delete", "/users/9", None),
    ],
)
def test_mutating_missing_user_returns_404(client, method, path, json):
    response = client.request(method, path, json=json)

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}


@pytest.mark.parametrize(
    "method,path,json",
    [
        ("post", "/users", {"id": 1, "name": "Ana", "roles": []}),
        ("put", "/users/1/roles", {"roles": ["admin"]}),
        ("patch", "/users/1", {"name": 123}),
    ],
)
def test_invalid_payload_returns_422(client, user_data, method, path, json):
    if method != "post":
        client.post("/users", json=user_data)

    response = client.request(method, path, json=json)

    assert response.status_code == 422
