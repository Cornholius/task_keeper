from dataclasses import dataclass
from sqlalchemy.orm import mapped_column, Mapped
from database.db import Base


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[str]
    owner: Mapped[str]
