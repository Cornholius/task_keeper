from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_async_session
from api.database.models import User, Task, UserTaskM2M
from api.auth.routers import current_user
from api.task.schemas import AddTaskSchema, PatchTaskSchema


router = APIRouter()


@router.get('/get/{pk}')
async def get_current_task(pk: int, session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    result = await session.get(Task, pk)
    if result.owner == user.email:
        return result
    else:
        return {"msg": "you don’t have access rights"}


@router.get('/get_all')
async def get_all_tasks(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    task_query = select(Task).where(Task.owner == user.email)
    shared_task_query = select(User).options(selectinload(User.task_list)).where(User.id == user.id)
    task_result = await session.scalars(task_query)
    shared_task_result = await session.scalars(shared_task_query)
    tasks: list = task_result.all()
    shared_tasks: list = shared_task_result.unique().one().task_list
    return tasks + shared_tasks


@router.post('/add')
async def add_new_task(request: AddTaskSchema, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_user)):
    try:
        # Создаем новую задачу
        new_task = Task(
            title=request.title,
            data=request.data,
            owner=user.email
        )

        # Добавляем задачу в сессию
        session.add(new_task)

        # Фиксируем изменения в базе данных
        await session.commit()

        # Обновляем объект new_task, чтобы получить его id и другие автоматически сгенерированные поля
        await session.refresh(new_task)

        # Создаем связь между пользователем и задачей через промежуточную таблицу UserTaskM2M
        user_task_m2m = UserTaskM2M(
            user_id=user.id,
            task_id=new_task.id
        )

        # Добавляем связь в сессию
        session.add(user_task_m2m)

        # Фиксируем изменения в базе данных
        await session.commit()

        return {"msg": "Запись успешно добавлена"}

    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch('/patch/{pk}')
async def patch_task(pk: int, task_data: PatchTaskSchema, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user)):
    old_task = await session.get(Task, pk)

    if not old_task:
        return {"msg": "Запись не найдена"}, 404

    if old_task.owner != user.email:
        return {"msg": "Нет доступа для обновления записи"}, 403

    # Преобразуем Pydantic модель в словарь
    update_data = task_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(old_task, key, value)

    session.add(old_task)
    await session.commit()

    return {"msg": "Запись успешно обновлена"}


@router.delete('/delete/{pk}')
async def delete_task(pk: int, session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    # Создаём запрос на удаление задачи с заданным идентификатором и владельцем
    query = (delete(Task).where((Task.id == pk) & (Task.owner == user.email)))

    try:
        # Выполняем асинхронный запрос на удаление задачи
        result = await session.execute(query)

        # Проверяем, сколько записей было удалено
        if not result.rowcount:
            return {"msg": "Запись не найдена"}, 404

        # Фиксируем изменения в базе данных
        await session.commit()

        return {"msg": "Запись успешно удалена"}

    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию и выводим сообщение об ошибке
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Не удалось удалить запись"
        )

@router.post('/share/')
async def share_task(pk: int, allowed_user_email: str, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user)):
    task = await session.get(Task, pk)
    if task.owner == user.email:
        user_query = select(User).where(User.email == allowed_user_email)
        allowed_user = await session.scalar(user_query)
        allowed_user.task_list.append(task)
        await session.commit()
