from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=True)
    data: Mapped[str]
    owner: Mapped[str]
