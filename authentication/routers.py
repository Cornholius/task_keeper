from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from authentication.schemas import UserCreate, UserRead
from authentication.auth import auth_backend, current_active_user, fastapi_users
from authentication.models import User
from database.db import get_async_session


router = APIRouter()
router.include_router(fastapi_users.get_auth_router(auth_backend), tags=["Аутентификация"])
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate), tags=["Регистрация"])


@router.get('/all_users')
async def all_users(session: AsyncSession = Depends(get_async_session)):
    statement = select(User)
    user_obj = await session.scalars(statement)
    return user_obj.all()


@router.get("/jwt-test")
def protected_route(user: User = Depends(current_active_user)):
    return f"Hello, {user.email}. You are authenticated with a JWT."
