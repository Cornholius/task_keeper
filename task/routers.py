from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import get_async_session
from database.models import User, Task
from auth.routers import current_user
from task.schemas import GetTaskSchema, AddTaskSchema, PatchTaskSchema


router = APIRouter()


@router.get('/get/{pk}')
async def get_current_task(pk: int, session: AsyncSession = Depends(get_async_session)):
    await session.get(Task, pk)
    return await session.get(Task, pk)


@router.get('/get_all')
async def get_all_tasks(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    query = select(Task).where(Task.owner == user.email)
    res = await session.execute(query)
    result = [GetTaskSchema.model_validate(row[0], from_attributes=True) for row in res.all()]
    return result


@router.post('/add')
async def add_new_task(request: AddTaskSchema, session: AsyncSession = Depends(get_async_session)):
    session.add(Task(**dict(request)))
    await session.commit()


@router.patch('/patch/{pk}')
async def patch_task(pk: int, task: PatchTaskSchema, session: AsyncSession = Depends(get_async_session)):
    old_data = await session.get(Task, pk)
    old_data.title = task.title
    old_data.data = task.data
    await session.commit()


@router.delete('/del/{pk}')
async def delete_task(pk: int, session: AsyncSession = Depends(get_async_session)):
    task = await session.get(Task, pk)
    await session.delete(task)
    await session.commit()
