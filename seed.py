import asyncio
import httpx
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, DateTime, ForeignKey, select
from typing import Optional

# API Configuration
API_URL = "http://localhost:8001"
API_KEY = "abc"
HEADERS = {"api-key": API_KEY}

# Database Configuration
DATABASE_URL = "postgresql+asyncpg://postgres:pgpasswd@localhost/postgres"
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# Database models
class Base(DeclarativeBase):
    pass

class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)

    statuses = relationship("SensorStatus", back_populates="sensor")

class SensorStatus(Base):
    __tablename__ = "sensor_status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    temperature: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dissolved_oxygen: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dissolved_oxygen_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    sensor = relationship("Sensor", back_populates="statuses")

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def fetch_sensors():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/sensors/list", headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("sensors", [])
        return []

async def fetch_sensor_status(sensor_id):
    start_date = datetime.utcfromtimestamp(0).isoformat() + "Z"
    end_date = datetime.utcnow().isoformat() + "Z"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{API_URL}/sensors/{sensor_id}/readings?start_date={start_date}&end_date={end_date}",
            headers=HEADERS
        )
        
        if response.status_code == 200:
            return response.json()
        
        print(response.text)
        return None
    

async def seed_database():
    async with AsyncSessionLocal() as session:
        sensors = await fetch_sensors()
        for sensor in sensors:
            result = await session.execute(select(Sensor).where(Sensor.id == sensor['id']))
            existing_sensor = result.scalar_one_or_none()
            if not existing_sensor:
                new_sensor = Sensor(id=sensor['id'], name=sensor['name'], location="Unknown")
                session.add(new_sensor)
                await session.commit()  # Commit after adding the sensor

            status = await fetch_sensor_status(sensor['id'])
            print(status)
            for reading in status["readings"]:
                new_status = SensorStatus(
                    sensor_id=sensor['id'],
                    timestamp=datetime.fromisoformat(reading['datetime']),
                    temperature=reading.get('temperature'),
                    dissolved_oxygen=reading.get('dissolved_oxygen'),
                    dissolved_oxygen_percent=reading.get('dissolved_oxygen_percent')
                )
                session.add(new_status)
        
        await session.commit()

async def main():
    await create_tables()
    await seed_database()
    print("Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(main())
