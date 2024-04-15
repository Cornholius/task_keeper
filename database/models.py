from pydantic import EmailStr
from fastapi_users.db import SQLAlchemyUserDatabase, SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean
from sqlalchemy.orm import relationship, mapped_column, Mapped, declarative_base, DeclarativeBase

metadata = MetaData()
# Base = declarative_base()


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str | None]
    data: Mapped[str]
    owner: Mapped[str]


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    hashed_password: Mapped[str]
    tasks_ids: Mapped[str]
    is_active: Mapped[bool] = mapped_column(insert_default=True)
    is_superuser: Mapped[bool] = mapped_column(insert_default=False)
    is_verified: Mapped[bool] = mapped_column(insert_default=False)
