from pydantic import BaseModel

from app.models import User


class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    roles: list[str]

    @classmethod
    def from_model(cls, user: User):
        return cls(
            id=user.id,
            name=user.name,
            password=user.password,
            roles=user.roles,
        )


class UserCreate(BaseModel):
    id: int
    name: str
    password: str
    roles: list[str]


class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None
