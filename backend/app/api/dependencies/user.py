from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.dependencies.database import DatabaseDep
from app.models import User
from app.services import user as user_service


def get_user_by_path(database: DatabaseDep, user_id: int) -> User:
    user = user_service.get_user(database, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


UserByPathDep = Annotated[User, Depends(get_user_by_path)]
