from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean


metadata = MetaData()

task = Table(
    'task',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String, nullable=False),
    Column('data', String),
    Column('owner', String)
)

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('email', String, nullable=False),
    Column('name', String),
    Column('hashed_password', String),
    Column('tasks_ids', String),
    Column('is_active', Boolean, default=True, nullable=False),
    Column('is_superuser', Boolean, default=True, nullable=False),
    Column('is_verified', Boolean, default=True, nullable=False),
)
