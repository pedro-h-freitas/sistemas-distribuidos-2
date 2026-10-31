from unittest.mock import Mock

from app.repositories import user as user_repository


def test_get_all_returns_users_from_query(user):
    result = Mock()
    result.scalars.return_value.all.return_value = [user]
    session = Mock()
    session.execute.return_value = result

    assert user_repository.get_all(session) == [user]
    session.execute.assert_called_once()


def test_get_by_id_returns_matching_user(user):
    session = Mock()
    session.execute.return_value.scalar_one_or_none.return_value = user

    assert user_repository.get_by_id(session, 1) is user
    session.execute.assert_called_once()


def test_create_adds_commits_and_refreshes_user(user):
    session = Mock()

    assert user_repository.create(session, user) is user

    session.add.assert_called_once_with(user)
    session.commit.assert_called_once_with()
    session.refresh.assert_called_once_with(user)


def test_update_roles_changes_and_persists_user(user):
    session = Mock()
    session.execute.return_value.scalar_one_or_none.return_value = user

    assert user_repository.update_roles(session, 1, ["admin"]) is user

    assert user.roles == ["admin"]
    session.commit.assert_called_once_with()
    session.refresh.assert_called_once_with(user)


def test_update_roles_returns_none_when_user_missing():
    session = Mock()
    session.execute.return_value.scalar_one_or_none.return_value = None

    assert user_repository.update_roles(session, 9, ["admin"]) is None

    session.commit.assert_not_called()


def test_update_user_changes_given_fields(user):
    session = Mock()

    assert user_repository.update_user(session, user, {"name": "Bia"}) is user

    assert user.name == "Bia"
    session.commit.assert_called_once_with()
    session.refresh.assert_called_once_with(user)


def test_delete_removes_and_commits_user(user):
    session = Mock()

    assert user_repository.delete(session, user) is None

    session.delete.assert_called_once_with(user)
    session.commit.assert_called_once_with()
