from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession
from api.database.database import get_async_session
from api.database.models import User, Task, UserTaskM2M
from api.auth.routers import current_user
from api.task.schemas import AddTaskSchema, PatchTaskSchema


router = APIRouter()


@router.get('/get/{pk}')
async def get_current_task(pk: int, session: AsyncSession = Depends(get_async_session),
                           user: User = Depends(current_user)):
    try:
        # Проверяем, существует ли связь между пользователем и задачей
        query = select(Task).join(UserTaskM2M).where((UserTaskM2M.user_id == user.id) & (Task.id == pk))
        result = await session.execute(query)
        task = result.scalars().first()

        if task is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Задача не найдена")

        return task

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/get_all')
async def get_all_tasks(session: AsyncSession = Depends(get_async_session), user: User = Depends(current_user)):
    try:
        # Получаем все задачи, принадлежащие пользователю
        task_query = select(Task).where(Task.owner == user.email)
        result_task = await session.execute(task_query)
        owned_tasks: list = result_task.scalars().all()

        # Получаем все задачи, разрешенные пользователю через промежуточную таблицу UserTaskM2M
        shared_task_query = (
            select(Task)
            .join(UserTaskM2M, Task.id == UserTaskM2M.task_id)
            .where(UserTaskM2M.user_id == user.id)
        )
        result_shared_tasks = await session.execute(shared_task_query)
        shared_tasks: list = result_shared_tasks.scalars().all()

        # Объединяем задачи и удаляем дубликаты
        all_tasks = owned_tasks + shared_tasks
        unique_tasks = list(set(all_tasks))

        return unique_tasks, status.HTTP_200_OK

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


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

        # Добавляем задачу в сессию и фиксируем изменения
        session.add(new_task)
        await session.commit()

        # Обновляем объект new_task, чтобы получить его id
        await session.refresh(new_task)

        # Создаем связь между пользователем и задачей через промежуточную таблицу UserTaskM2M
        user_task_m2m = UserTaskM2M(
            user_id=user.id,
            task_id=new_task.id
        )

        # Добавляем связь в сессию и фиксируем изменения
        session.add(user_task_m2m)
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
async def delete_task(pk: int, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_user)):
    try:
        # Проверяем, является ли пользователь владельцем задачи
        owner_query = select(Task).where((Task.id == pk) & (Task.owner == user.email))
        result_owner = await session.execute(owner_query)
        task = result_owner.scalars().first()

        if task is not None and task.owner == user.email:
            # Если пользователь является владельцем, удаляем задачу
            delete_task_query = delete(Task).where((Task.id == pk) & (Task.owner == user.email))
            await session.execute(delete_task_query)
            await session.commit()
            return {"msg": "Запись успешно удалена"}, status.HTTP_200_OK
        else:
            # Если пользователь не является владельцем, удаляем связь между задачей и пользователем
            delete_relation_query = delete(UserTaskM2M).where((UserTaskM2M.user_id == user.id) &
                                                              (UserTaskM2M.task_id == pk))
            await session.execute(delete_relation_query)
            await session.commit()
            return {"msg": "Связь с задачей удалена"}, status.HTTP_200_OK

    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию и выводим сообщение об ошибке
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось удалить запись. Причина: {e}"
        )


@router.post('/share/')
async def share_task(pk: int, allowed_user_email: str,
                     session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(current_user)):
    try:
        # Проверяем, что пользователь является владельцем задачи
        task_query = select(Task).where((Task.id == pk) & (Task.owner == user.email))
        result_task = await session.execute(task_query)
        task = result_task.scalars().first()

        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Задача не найдена или вы не являетесь её владельцем.")

        # Проверяем, что пользователь с указанным email существует
        user_query = select(User).where(User.email == allowed_user_email)
        result_user = await session.execute(user_query)
        allowed_user = result_user.scalars().first()

        if not allowed_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Пользователь не найден.")

        # Проверяем, что связь уже не существует
        relation_query = select(UserTaskM2M).where(
            (UserTaskM2M.user_id == allowed_user.id) & (UserTaskM2M.task_id == pk)
        )
        result_relation = await session.execute(relation_query)
        existing_relation = result_relation.scalars().first()

        if existing_relation:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="Пользователь уже имеет доступ к этой задаче.")

        # Создаем новую связь между пользователем и задачей
        insert_query = insert(UserTaskM2M).values(
            user_id=allowed_user.id,
            task_id=pk
        )
        await session.execute(insert_query)
        await session.commit()

        return {"msg": "Задача успешно разрешена пользователю"}, status.HTTP_201_CREATED

    except Exception as e:
        # Если произошла ошибка, откатываем транзакцию и выводим сообщение об ошибке
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Не удалось разрешить задачу пользователю. Причина: {e}"
        )
