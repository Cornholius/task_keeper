from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead
from auth.auth import auth_backend
from database.database import get_async_session
from database.database import User


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
router = APIRouter()
router.include_router(fastapi_users.get_auth_router(auth_backend), tags=["Аутентификация"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), tags=["Регистрация"])
current_user = fastapi_users.current_user()


@router.get('/all_users', tags=['Пользователи'])
async def all_users(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if user.is_superuser:
        statement = select(User)
        user_obj = await session.scalars(statement)
        return user_obj.all()
    else:
        return {"status": 401, "message": "you are not superuser"}


@router.get("/protected-route")
def ololo(user: User = Depends(current_user)):
    return f"Hello, {user.name}"
