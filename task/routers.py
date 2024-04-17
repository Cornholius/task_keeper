import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from database.db import get_async_session
from task.models import Task
from task.schemas import getTask, addTask


router = APIRouter()


@router.get('/get/{pk}')
async def get_current_task(pk: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.id == pk)
    res = await session.execute(query)
    result = getTask.model_validate(*res.one_or_none(), from_attributes=True)
    return result


@router.get('/get_all')
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(Task)
    res = await session.execute(query)
    result = [getTask.model_validate(row[0], from_attributes=True) for row in res.all()]
    return result


@router.post('/add')
async def new_task(request: addTask, session: AsyncSession = Depends(get_async_session)):
    qwe = [*request]
    print('!!!!!/add', qwe)
    # data = json.loads(request)
    session.add(Task(*request))
    await session.commit()


@router.patch('/patch/')
async def new_task(task: getTask, session: AsyncSession = Depends(get_async_session)):
    old_data = await session.get(Task, task.id)
    for key, value in task:
        setattr(old_data, key, value)
    await session.commit()


@router.delete('/del/')
async def new_task(request, session: AsyncSession = Depends(get_async_session)):
    data = json.loads(request)
