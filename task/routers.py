from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_async_session
from database.models import User, Task
from auth.routers import current_user
from task.schemas import AddTaskSchema, PatchTaskSchema


router = APIRouter()


@router.get('/get/{pk}')
async def get_current_task(pk: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    result = await session.get(Task, pk)
    if result.owner == user.email:
        return result
    else:
        return {"msg": "you don’t have access rights"}


@router.get('/get_all')
async def get_all_tasks(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    query = select(Task).where(Task.owner == user.email)
    result = await session.scalars(query)
    return result.all()


@router.post('/add')
async def add_new_task(request: AddTaskSchema, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    session.add(Task(
        title=request.title,
        data=request.data,
        owner=user.email)
    )
    await session.commit()


@router.patch('/patch/{pk}')
async def patch_task(pk: int, task: PatchTaskSchema, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user)):
    old_data = await session.get(Task, pk)
    if old_data.owner == user.email:
        for key, value in task:
            setattr(old_data, key, value)
        await session.commit()
        return {"msg": "Запись успешно обновлена"}


@router.delete('/del/{pk}')
async def delete_task(pk: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    task = await session.get(Task, pk)
    if task.owner == user.email:
        await session.delete(task)
        await session.commit()
        return {"msg": f"Запись {task.title} удалена"}
