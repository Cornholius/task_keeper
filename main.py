from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from database.models import User
from auth.manager import get_user_manager
# from auth.router import router as auth_router
from auth.schemas import UserCreate, UserRead
from database.db import async_session_maker
from sqlalchemy import select


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


@app.get('/all_users')
async def all_users():
    async with async_session_maker() as session:
        result = await session.execute(select(User))
        # result = await session.query(User)
    for i in result.all():
        print(i, type(i))
