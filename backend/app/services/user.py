from sqlalchemy.orm import Session

from app.models import User
from app.repositories import user as user_repository


def get_users(session: Session) -> list[User]:
    return user_repository.get_all(session)


def get_user(session: Session, user_id: int) -> User | None:
    return user_repository.get_by_id(session, user_id)


def create_user(
    session: Session, id: int, name: str, password: str, roles: list[str]
) -> User:
    user_exists = user_repository.get_by_id(session, id) is not None
    if user_exists:
        return None

    user = User(
        id=id,
        name=name,
        password=password,
        roles=roles,
    )

    user = user_repository.create(session, user)
    return user


def update_user_roles(session: Session, user: User, roles: list[str]) -> User:
    user = user_repository.update_roles(session, user.id, roles)
    return user


def update_user(
    session: Session,
    user: User,
    fields: dict,
) -> User:
    user = user_repository.update_user(session, user, fields)
    return user


def delete_user(session: Session, user: dict) -> None:
    user_repository.delete(session, user)
    return
