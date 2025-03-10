import asyncio
import os
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Float, DateTime, ForeignKey
import gmqtt

# Retrieve environment variables
DB_URL = os.getenv("POSTGRES_URL")  # Format: postgresql+asyncpg://user:password@host/dbname
MQTT_BROKER = os.getenv("MQTT_BROKER")
MQTT_CLIENT_ID = "mqtt_client"

assert DB_URL, "POSTGRES_URL environment variable is not set."
assert MQTT_BROKER, "MQTT_BROKER environment variable is not set."

# Database setup
engine = create_async_engine(DB_URL, echo=True)
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

# Define database models
class Base(DeclarativeBase):
    pass

class Sensor(Base):
    __tablename__ = "sensors"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    location: Mapped[str] = mapped_column(String, nullable=False)  # GPS coordinates

    statuses = relationship("SensorStatus", back_populates="sensor")

class SensorStatus(Base):
    __tablename__ = "sensor_status"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sensor_id: Mapped[str] = mapped_column(ForeignKey("sensors.id"), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)  # Renamed from `datetime`

    temperature: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dissolved_oxygen: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    dissolved_oxygen_percent: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    sensor = relationship("Sensor", back_populates="statuses")

# Define Pydantic model for validation
class SensorData(BaseModel):
    timestamp: datetime
    sensor: str
    temperature: float = Field(..., gt=-50, lt=100)
    dissolved_oxygen: float = Field(..., gt=0, lt=20)

# MQTT client setup
client = gmqtt.Client(MQTT_CLIENT_ID)

def on_connect(client, flags, rc, properties):
    print("Connected to MQTT broker.")
    client.subscribe("sensor/#")

def on_disconnect(client, packet, exc=None):
    print("Disconnected from MQTT broker, attempting to reconnect...")
    asyncio.create_task(client.reconnect())

def on_message(client, topic, payload, qos, properties):
    asyncio.create_task(process_message(topic, payload))

client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect

async def save_sensor_status(session: AsyncSession, sensor_data: SensorData):
    sensor = await session.get(Sensor, sensor_data.sensor)
    if not sensor:
        sensor = Sensor(id=sensor_data.sensor, name=f"Sensor {sensor_data.sensor}", location="Unknown")
        session.add(sensor)
        await session.commit()

    status = SensorStatus(
        sensor_id=sensor_data.sensor,
        datetime=sensor_data.timestamp,
        temperature=sensor_data.temperature,
        dissolved_oxygen=sensor_data.dissolved_oxygen,
        dissolved_oxygen_percent=None,  # Calculate if necessary
    )
    session.add(status)
    await session.commit()

async def process_message(topic, payload):
    try:
        p = payload.decode("utf-8").strip()
        if topic.startswith("sensor/") and p.startswith("{") and p.endswith("}"):
            p = p[1:-1]
            dat = [x.strip() for x in p.split(",") if x.strip()]

            if len(dat) < 7:
                print("Invalid payload received:", p)
                return

            date, time, sensor, _, temp, _, diox = dat
            ts = f"20{date[6:8]}-{date[3:5]}-{date[0:2]}T{time}"

        else:
            print(f"Unknown topic format: {topic}")
            return

        sensor_data = SensorData(
            timestamp=datetime.fromisoformat(ts),
            sensor=sensor,
            temperature=float(temp),
            dissolved_oxygen=float(diox),
        )

        async with SessionLocal() as session:
            await save_sensor_status(session, sensor_data)

        print(f"Saved sensor data: {sensor_data}")

    except (ValueError, ValidationError) as e:
        print(f"Error processing message: {e}")

async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Ensure tables exist

async def mqtt_loop():
    await client.connect(MQTT_BROKER)
    await asyncio.Future()  # Keep the loop running

async def main():
    await setup_database()
    await mqtt_loop()

if __name__ == "__main__":
    asyncio.run(main())
