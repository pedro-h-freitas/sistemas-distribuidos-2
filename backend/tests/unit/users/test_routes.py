from unittest.mock import Mock, patch

import pytest
from fastapi import HTTPException

from app.api.routes import users
from app.schemas.user import UserCreate, UserUpdate


def test_get_users_converts_service_result_to_response(database, user):
    with patch.object(
        users.user_service, "get_users", return_value={1: user}
    ) as service:
        result = users.get_users(database)

    service.assert_called_once_with(database)
    assert [item.model_dump() for item in result] == [user]


def test_get_user_uses_resolved_user(user):
    assert users.get_user(user).model_dump() == user


def test_create_user_passes_payload_to_service(database, user):
    payload = UserCreate(**user)
    with patch.object(users.user_service, "create_user", return_value=user) as service:
        result = users.create_user(payload, database)

    service.assert_called_once_with(
        database, id=1, name="Ana", password="secret", roles=["reader"]
    )
    assert result.model_dump() == user


def test_create_user_raises_409_on_duplicate(database, user):
    with patch.object(users.user_service, "create_user", return_value=None):
        with pytest.raises(HTTPException) as error:
            users.create_user(UserCreate(**user), database)

    assert error.value.status_code == 409


def test_update_user_roles_passes_roles_to_service(database, user):
    updated = {**user, "roles": ["admin"]}
    with patch.object(
        users.user_service, "update_user_roles", return_value=updated
    ) as service:
        result = users.update_user_roles(database, user, ["admin"])

    service.assert_called_once_with(database, user, roles=["admin"])
    assert result.model_dump() == updated


def test_update_user_passes_only_supplied_fields(database, user):
    updated = {**user, "name": "Bia"}
    with patch.object(
        users.user_service, "update_user", return_value=updated
    ) as service:
        result = users.update_user(database, user, UserUpdate(name="Bia"))

    service.assert_called_once_with(database, user, fields={"name": "Bia"})
    assert result.model_dump() == updated


def test_delete_user_calls_service(database, user):
    service = Mock()
    with patch.object(users.user_service, "delete_user", service):
        assert users.delete_user(database, user) is None

    service.assert_called_once_with(database, user)
