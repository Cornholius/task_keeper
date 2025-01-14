from typing import Optional
from pydantic import BaseModel, Field, EmailStr


# Определение общих типов для повторного использования
TaskData = str  # Например, задача может содержать строку данных
TaskTitle = Optional[str]  # Заголовок задачи является необязательным
OwnerId = EmailStr  # Идентификатор владельца задачи (например, email)


class TaskBaseSchema(BaseModel):
    title: TaskTitle = Field(None, description="Заголовок задачи (опционально)")
    data: TaskData = Field(..., description="Текст задачи")

    class Config:
        orm_mode = True


class GetTaskSchema(TaskBaseSchema):
    id: int = Field(..., description="Уникальный идентификатор для задачи")
    owner: OwnerId = Field(..., description="Владелец задачи (в формате email)")


class AddTaskSchema(TaskBaseSchema):
    pass


class PatchTaskSchema(TaskBaseSchema):
    pass
