from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import json
from database.db import async_session_maker, get_async_session
from task.models import Task
from task.schemas import Task as TaskSchema


router = APIRouter()


@router.get('/get_all')
async def get_all_tasks(session: AsyncSession = Depends(get_async_session)):
    query = select(Task).where(Task.owner == 'Corn')
    result = await session.execute(query)
    # return json.dumps(result.all())
    result_dto = [TaskSchema.model_validate(row, from_attributes=True) for row in result.all()]
    print(result_dto)
    return result_dto


@router.post('/add')
async def new_task(request):
    print(request.JSON)
    # print(title, data, owner)
    async with async_session_maker() as session:
        task = Task(request.name, request.data, request.owner)
        session.add(task)
        await session.commit()
    print('added new task')
