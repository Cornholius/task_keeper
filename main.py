from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from auth.auth import auth_backend
from auth.database import User
from auth.manager import get_user_manager
# from auth.router import router as auth_router
from auth.schemas import UserCreate, UserRead


app = FastAPI(title='Заметки')
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

# app.include_router(auth_router)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)