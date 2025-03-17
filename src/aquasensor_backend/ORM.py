import os
import asyncio
from functools import partial
from datetime import datetime, timezone

from loguru import logger
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, MetaData
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
DATABASE_ECHO = bool(os.getenv("DATABASE_ECHO", False))

async_engine = create_async_engine(DATABASE_URL, echo=DATABASE_ECHO, future=True)

metadata = MetaData()
Base = declarative_base(metadata=metadata)

current_utc_datetime = partial(datetime.now, timezone.utc)

class Users(Base):
    __tablename__ = "users"

    uid: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)

class Rivers(Base):
    __tablename__ = "Rivers"

    RiverId: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)

class Sensors(Base):
    __tablename__ = "Sensors"

    id: Mapped[str] = mapped_column(String(32), primary_key=True)
    RiverId: Mapped[int] = mapped_column(Integer, ForeignKey("Rivers.RiverId"), nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    name: Mapped[str] = mapped_column(String(32), nullable=False)

    readings = relationship("SensorReadings", back_populates="sensor")

class SensorReadings(Base):
    __tablename__ = "SensorReadings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(String(32), ForeignKey("Sensors.id"))
    temperature: Mapped[int] = mapped_column(Integer, nullable=True)
    dissolved_oxygen: Mapped[int] = mapped_column(Integer, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=current_utc_datetime)

    sensor = relationship("Sensors", back_populates="readings")

# Session factory
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

async def init_db():
    """Create all tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)

if __name__ == "__main__":
    asyncio.run(init_db())
