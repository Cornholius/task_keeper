from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(insert_default=True)
    is_superuser: Mapped[bool] = mapped_column(insert_default=False)
    is_verified: Mapped[bool] = mapped_column(insert_default=False)

    task_list: Mapped[list["Task"]] = relationship(
        back_populates="user_list",
        secondary="UserTaskM2M",
        lazy="joined"
    )


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[str]
    owner: Mapped[str]

    user_list: Mapped[list["User"]] = relationship(
        back_populates="task_list",
        secondary="UserTaskM2M",
    )


class UserTaskM2M(Base):
    __tablename__ = 'UserTaskM2M'

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'), primary_key=True)
    task_id: Mapped[int] = mapped_column(ForeignKey('task.id', ondelete='CASCADE'), primary_key=True)
