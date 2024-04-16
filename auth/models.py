from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column
from database.db import Base


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
