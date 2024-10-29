from fastapi import FastAPI
from api.task.routers import router as task_router
from api.auth.routers import router as auth_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title='Заметки')

origins = ["http://127.0.0.1:3000", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Аутентификация и регистрация"])
app.include_router(task_router, prefix='/tasks', tags=['Задачи'])
