from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    name: str
    password: str
    roles: list[str]


class UserCreate(BaseModel):
    id: int
    name: str
    password: str
    roles: list[str]


class UserUpdate(BaseModel):
    name: str | None = None
    password: str | None = None
