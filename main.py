from fastapi import FastAPI
from task.routers import router as task_router
from auth.routers import router as auth_router


app = FastAPI(title='Заметки')

app.include_router(auth_router, prefix="/auth")
app.include_router(task_router, prefix='/tasks', tags=['Задачи'])
