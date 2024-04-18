import uvicorn
from fastapi import FastAPI
from task.routers import router as task_router
from authentication.routers import router as auth_router


app = FastAPI(title='Заметки')


app.include_router(task_router, prefix='/tasks', tags=['Задачи'])
app.include_router(auth_router, prefix="/auth")

if __name__ == '__main__':
    uvicorn.run(app='main:app', host="10.10.10.64", port=8000, reload=True)
