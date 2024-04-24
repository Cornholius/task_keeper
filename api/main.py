from fastapi import FastAPI
from api.task.routers import router as task_router
from api.auth.routers import router as auth_router


app = FastAPI(title='Заметки')

app.include_router(auth_router, prefix="/auth", tags=["Аутентификация и регистрация"])
app.include_router(task_router, prefix='/tasks', tags=['Задачи'])
