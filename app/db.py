import datetime
import os
import uuid

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")


class Posts(DeclarativeBase):
    __tablename__ = "Posts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    caption = Column(Text)
    url = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


engine = create_async_engine(DATABASE_URL)

async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_table():
    async with engine.begin() as conn:
        await conn.run_sync(DeclarativeBase.metadata.create_all)


async def get_async_session():
    async with async_sessionmaker() as session:
        yield session
