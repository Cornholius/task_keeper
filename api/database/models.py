from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


# Определение базового класса для моделей
class Base(DeclarativeBase):
    pass


# Модель пользователя
class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    name: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)

    task_list: Mapped[list["Task"]] = relationship(
        back_populates="user",
        secondary="UserTaskM2M",
        lazy="selectin",
    )


# Модель задачи
class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    data: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    user: Mapped["User"] = relationship(
        back_populates="task_list",
        foreign_keys=[owner_id],
        lazy="selectin",
    )


# Модель связи многие-ко-многим между пользователями и задачами
class UserTaskM2M(Base):
    __tablename__ = 'UserTaskM2M'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id', ondelete='CASCADE'), primary_key=True)
