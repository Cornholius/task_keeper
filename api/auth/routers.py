from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from api.auth.manager import get_user_manager
from api.auth.schemas import UserCreate, UserRead
from api.auth.auth import auth_backend
from api.database.database import get_async_session
from api.database.database import User


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])
router = APIRouter()
router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
current_user = fastapi_users.current_user()


@router.get('/all_users', tags=['Пользователи'])
async def all_users(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    if not user.is_superuser:
        statement = select(User)
        # user_obj = await session.scalars(statement)
        result = await session.execute(statement)
        user_obj = result.unique().scalars().all()
        for i in user_obj:
            print(i.name, i.task_list)
        return user_obj
    else:
        return {"status": 401, "message": "you are not superuser"}


@router.get('/user', tags=['Пользователи'])
async def user(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    print(session)
    print(user)
    if not user.is_superuser:
        statement = select(User)
        print(statement)
        # user_obj = await session.scalars(statement)
        result = await session.execute(statement)
        print(result)
        user_obj = result.unique().scalars().first()
        # for i in user_obj:
        #     print(i.name, i.task_list)
        return user_obj
    else:
        return {"status": 401, "message": "you are not superuser"}
