from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.database import DatabaseDep
from app.api.dependencies.user import UserByPathDep
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services import user as user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_users(session: DatabaseDep) -> list[UserResponse]:
    users = user_service.get_users(session)
    return [UserResponse.from_model(user) for user in users]


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def get_user(user: UserByPathDep) -> UserResponse:
    return UserResponse.from_model(user)


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, session: DatabaseDep) -> UserResponse:
    user = user_service.create_user(
        session,
        id=payload.id,
        name=payload.name,
        password=payload.password,
        roles=payload.roles,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exisits"
        )

    return UserResponse.from_model(user)


@router.put(
    "/{user_id}/roles", response_model=UserResponse, status_code=status.HTTP_200_OK
)
def update_user_roles(
    session: DatabaseDep, user: UserByPathDep, payload: list[str]
) -> UserResponse:
    user = user_service.update_user_roles(session, user, roles=payload)
    return UserResponse.from_model(user)


@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(
    session: DatabaseDep,
    user: UserByPathDep,
    payload: UserUpdate,
) -> UserResponse:
    user = user_service.update_user(
        session, user, fields=payload.model_dump(exclude_none=True)
    )
    return UserResponse.from_model(user)


@router.delete(
    "/{user_id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT
)
def delete_user(session: DatabaseDep, user: UserByPathDep) -> None:
    user_service.delete_user(session, user)
    return
