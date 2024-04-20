from typing import Optional
from pydantic import BaseModel


class GetTaskSchema(BaseModel):
    id: int
    title: Optional[str]
    data: str
    owner: str


class AddTaskSchema(BaseModel):
    title: Optional[str]
    data: str
    owner: str


class PatchTaskSchema(BaseModel):
    title: Optional[str] = None
    data: Optional[str] = None
