from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import User


def get_all(session: Session) -> list[User]:
    stmt = select(User)
    result = session.execute(stmt).scalars().all()
    return list(result)


def get_by_id(session: Session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt).scalar_one_or_none()
    return result


def create(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def update_roles(session: Session, user_id: int, roles: list[str]) -> User:
    user = get_by_id(session, user_id)
    if user is None:
        return None

    user.roles = roles
    session.commit()
    session.refresh(user)
    return user


def update_user(session: Session, user: User, fields: dict) -> User:
    for field, value in fields.items():
        setattr(user, field, value)

    session.commit()
    session.refresh(user)
    return user


def delete(session: Session, user: User) -> None:
    session.delete(user)
    session.commit()
