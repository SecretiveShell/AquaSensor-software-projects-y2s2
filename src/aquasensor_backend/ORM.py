import os
import asyncio
from functools import partial
from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.ext.asyncio import async_sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', "sqlite+aiosqlite:///:memory:")
DATABASE_ECHO = bool(os.getenv('DATABASE_ECHO', False))

async_engine = create_async_engine(DATABASE_URL, echo=DATABASE_ECHO)

metadata = MetaData()
Base = declarative_base(metadata=metadata)

current_utc_datetime = partial(datetime.now, timezone.utc)

class Users(Base):
    __tablename__ = 'users'

    uid: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

class RiverData(Base):
    __tablename__ = 'RiverData'

    RiverId: Mapped[int] = mapped_column(Integer, primary_key=True)
    Rivertemp: Mapped[int] = mapped_column(Integer)
    DOlevels: Mapped[int] = mapped_column(Integer)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=current_utc_datetime, onupdate=current_utc_datetime
    )

# session factory
AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

async def init_db():
    """create all tables"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



if __name__ == "__main__":
    asyncio.run(init_db())
