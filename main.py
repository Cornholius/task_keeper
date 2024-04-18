import uvicorn
from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select

from auth.auth import auth_backend
from auth.manager import get_user_manager
from auth.models import User
from auth.schemas import UserCreate, UserRead
from database.db import async_session_maker, get_async_session
from task.routers import router as task_router
from sqlalchemy.ext.asyncio import AsyncSession


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

app.include_router(task_router, prefix='/tasks', tags=['Задачи'])


@app.get('/all_users')
async def all_users(session: AsyncSession = Depends(get_async_session)):
    statement = select(User)
    user_obj = await session.scalars(statement)
    return user_obj.all()


if __name__ == '__main__':
    uvicorn.run(app='main:app', host="10.10.10.64", port=8000, reload=True)
