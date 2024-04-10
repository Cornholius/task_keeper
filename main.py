from fastapi import FastAPI
from auth.router import router as auth_router


app = FastAPI(title='Заметки')


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

app.include_router(auth_router)
