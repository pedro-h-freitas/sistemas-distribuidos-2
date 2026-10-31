from unittest.mock import Mock, patch

from app.models import User
from app.services import user as user_service


def test_get_users_delegates_to_repository():
    session = Mock()
    expected = [User(id=1, name="Ana", password="secret", roles=["reader"])]
    with patch(
        "app.services.user.user_repository.get_all", return_value=expected
    ) as repo:
        assert user_service.get_users(session) is expected
    repo.assert_called_once_with(session)


def test_get_user_delegates_to_repository(user):
    session = Mock()
    with patch(
        "app.services.user.user_repository.get_by_id", return_value=user
    ) as repo:
        assert user_service.get_user(session, 1) is user
    repo.assert_called_once_with(session, 1)


def test_get_user_returns_none_when_missing():
    with patch("app.services.user.user_repository.get_by_id", return_value=None):
        assert user_service.get_user(Mock(), 9) is None


def test_create_user_persists_new_user(user):
    session = Mock()
    with (
        patch("app.services.user.user_repository.get_by_id", return_value=None),
        patch("app.services.user.user_repository.create", return_value=user) as create,
    ):
        result = user_service.create_user(
            session, id=1, name="Ana", password="secret", roles=["reader"]
        )
    assert result is user
    create.assert_called_once()
    assert create.call_args.args[0] is session
    assert create.call_args.args[1].id == 1


def test_create_user_does_not_replace_existing_user(user):
    session = Mock()
    with (
        patch("app.services.user.user_repository.get_by_id", return_value=user),
        patch("app.services.user.user_repository.create") as create,
    ):
        assert (
            user_service.create_user(
                session, id=1, name="Bia", password="new", roles=["admin"]
            )
            is None
        )
    create.assert_not_called()


def test_update_user_roles_delegates_to_repository(user):
    with patch(
        "app.services.user.user_repository.update_roles", return_value=user
    ) as repo:
        assert user_service.update_user_roles(Mock(), user, ["admin"]) is user
    repo.assert_called_once_with(repo.call_args.args[0], user.id, ["admin"])


def test_update_user_delegates_fields_to_repository(user):
    fields = {"name": "Bia", "password": "new"}
    with patch(
        "app.services.user.user_repository.update_user", return_value=user
    ) as repo:
        assert user_service.update_user(Mock(), user, fields) is user
    assert repo.call_args.args[1:] == (user, fields)


def test_update_user_passes_fields_through(user):
    with patch(
        "app.services.user.user_repository.update_user", return_value=user
    ) as repo:
        user_service.update_user(Mock(), user, {"unknown": "value"})
    assert repo.call_args.args[2] == {"unknown": "value"}


def test_delete_user_delegates_to_repository(user):
    with patch("app.services.user.user_repository.delete") as repo:
        assert user_service.delete_user(Mock(), user) is None
    repo.assert_called_once_with(repo.call_args.args[0], user)
