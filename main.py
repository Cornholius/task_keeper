from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserCreate, UserRead
from database.db import async_session_maker
from task.routers import router as TaskRouter


app = FastAPI(title='Заметки')
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Аутентификация"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Регистрация"],
)

app.include_router(TaskRouter, prefix='/tasks', tags=['Задачи'])


@app.get('/all_users')
async def all_users():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        # result = await session.query(User)
    for i in result.all():
        print(i, type(i))
