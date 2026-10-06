from unittest.mock import MagicMock, Mock, call

import pytest

from app.services import user as user_service


def test_get_users_returns_database_users(user):
    users = {1: user}
    database = Mock(spec=dict)
    database.get.return_value = users

    assert user_service.get_users(database) is users
    database.get.assert_called_once_with("users")


def test_get_user_returns_matching_user(user):
    users = Mock(spec=dict)
    users.get.return_value = user
    database = Mock(spec=dict)
    database.get.return_value = users

    assert user_service.get_user(database, 1) is user
    database.get.assert_called_once_with("users")
    users.get.assert_called_once_with(1)


def test_get_user_returns_none_when_missing():
    users = Mock(spec=dict)
    users.get.return_value = None
    database = Mock(spec=dict)
    database.get.return_value = users

    assert user_service.get_user(database, 9) is None
    users.get.assert_called_once_with(9)


def test_create_user_stores_new_user(user):
    users = MagicMock(spec=dict)
    users.get.return_value = None
    database = {"users": users}

    result = user_service.create_user(
        database, id=1, name="Ana", password="secret", roles=["reader"]
    )

    assert result == user
    users.get.assert_called_once_with(1)
    users.__setitem__.assert_called_once_with(1, user)


def test_create_user_does_not_replace_existing_user(user):
    users = MagicMock(spec=dict)
    users.get.return_value = user
    database = {"users": users}

    result = user_service.create_user(
        database, id=1, name="Bia", password="new", roles=["admin"]
    )

    assert result is None
    users.get.assert_called_once_with(1)
    users.__setitem__.assert_not_called()


def test_update_user_roles_changes_stored_user(user):
    stored = user.copy()
    users = MagicMock(spec=dict)
    users.__getitem__.return_value = stored

    result = user_service.update_user_roles({"users": users}, user, ["admin"])

    assert result is stored
    assert stored["roles"] == ["admin"]
    assert users.__getitem__.call_args_list == [call(1), call(1)]


def test_update_user_changes_only_requested_fields(user):
    stored = user.copy()
    users = MagicMock(spec=dict)
    users.__getitem__.return_value = stored

    result = user_service.update_user(
        {"users": users}, user, fields={"name": "Bia", "password": "new"}
    )

    assert result is stored
    assert stored == {**user, "name": "Bia", "password": "new"}
    assert users.__getitem__.call_args_list == [call(1), call(1), call(1)]


def test_update_user_rejects_unknown_fields_without_mutating(user):
    users = MagicMock(spec=dict)

    with pytest.raises(ValueError, match="Non-existent fields"):
        user_service.update_user({"users": users}, user, fields={"unknown": "value"})

    users.__getitem__.assert_not_called()


def test_delete_user_removes_matching_id(user):
    users = Mock(spec=dict)

    assert user_service.delete_user({"users": users}, user) is None
    users.pop.assert_called_once_with(1)
