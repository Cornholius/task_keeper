from typing import Optional
from pydantic import EmailStr, BaseModel


class Task(BaseModel):
    id: int
    title: str
    data: str
    owner: str
