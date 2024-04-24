from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    id: int
    name: str
    email: EmailStr


class UserCreate(schemas.BaseUserCreate):
    name: str
    email: EmailStr
    password: str
