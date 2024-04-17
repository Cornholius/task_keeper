import json
from fastapi import APIRouter, Depends, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_async_session
from task.models import Task
from task.schemas import Task as TaskSchema


router = APIRouter()


@router.get('/get/{pk}')
async def get_current_task(pk: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.id == pk)
    res = await session.execute(query)
    result = TaskSchema.model_validate(*res.one_or_none(), from_attributes=True)
    return result


@router.get('/get_all')
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(Task)
    res = await session.execute(query)
    result = [TaskSchema.model_validate(row[0], from_attributes=True) for row in res.all()]
    return result


@router.post('/add')
async def new_task(request, session: AsyncSession = Depends(get_async_session)):
    data = json.loads(request)
    session.add(Task(**data))
    await session.commit()


@router.patch('/patch/')
async def new_task(request: Request, session: AsyncSession = Depends(get_async_session)):
    print('!!!!!!!!!!!!!!!', request, type(request))
    data = json.loads(request)
    req = TaskSchema.model_validate(data)
    qwe = await session.execute(select(Task).where(Task.id == req.id))
    old_data = qwe.one()
    for key, value in data.items():
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        print(old_data, type(old_data))
        setattr(old_data, key, value)
    await session.commit()
    return old_data


@router.delete('/del/')
async def new_task(request, session: AsyncSession = Depends(get_async_session)):
    data = json.loads(request)
