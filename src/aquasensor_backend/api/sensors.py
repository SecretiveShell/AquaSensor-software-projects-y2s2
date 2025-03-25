from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from aquasensor_backend.ORM import AsyncSessionLocal
from aquasensor_backend.api.utils import do_saturation_percent
from aquasensor_backend.security import get_logged_in_user_depends
from aquasensor_backend.models.sensor import (
    SensorListResponse,
    SensorStatus,
    SensorStatusResponse,
    SensorReadingsResponse,
    SensorReadings,
)
from aquasensor_backend.ORM import Sensors, SensorReadings as SensorReadingsModel

router = APIRouter()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get("/status")
async def get_sensor_status(
    logged_in_user: get_logged_in_user_depends,
    db: AsyncSession = Depends(get_db),
) -> SensorStatusResponse:
    """Get sensor status with latest readings."""
    result = await db.execute(select(Sensors))
    sensors = result.scalars().all()

    response = []
    for sensor in sensors:
        latest_reading_result = await db.execute(
            select(SensorReadingsModel)
            .filter(SensorReadingsModel.sensor_id == sensor.id)
            .order_by(SensorReadingsModel.timestamp.desc())
            .limit(1)
        )
        latest_reading = latest_reading_result.scalar()

        response.append(
            SensorStatus(
                id=sensor.id,
                name=sensor.name,
                datetime=latest_reading.timestamp
                if latest_reading
                else datetime.utcnow(),
                temperature=latest_reading.temperature if latest_reading else None,
                dissolved_oxygen=latest_reading.dissolved_oxygen
                if latest_reading
                else None,
                dissolved_oxygen_percent=None,
            )
        )
    return SensorStatusResponse(sensors=response)


@router.get("/{sensorid}/status")
async def get_sensor_status_by_id(
    logged_in_user: get_logged_in_user_depends,
    sensorid: str,
    db: AsyncSession = Depends(get_db),
) -> SensorStatus:
    """Get sensor status by ID with latest readings."""
    result = await db.execute(select(Sensors).filter_by(id=sensorid))
    sensor = result.scalar()
    if not sensor:
        return None

    latest_reading_result = await db.execute(
        select(SensorReadingsModel)
        .filter(SensorReadingsModel.sensor_id == sensorid)
        .order_by(SensorReadingsModel.timestamp.desc())
        .limit(1)
    )
    latest_reading = latest_reading_result.scalar()

    return SensorStatus(
        id=sensor.id,
        name=sensor.name,
        datetime=latest_reading.timestamp if latest_reading else datetime.utcnow(),
        temperature=latest_reading.temperature if latest_reading else None,
        dissolved_oxygen=latest_reading.dissolved_oxygen if latest_reading else None,
        dissolved_oxygen_percent=do_saturation_percent(latest_reading.temperature, latest_reading.dissolved_oxygen) if latest_reading else None,
    )


@router.get("/{sensorid}/readings")
async def get_sensor_readings_by_id(
    logged_in_user: get_logged_in_user_depends,
    sensorid: str,
    start_date: datetime = Query(...),
    end_date: datetime = Query(...),
    db: AsyncSession = Depends(get_db),
) -> SensorReadingsResponse:
    """Get sensor readings by ID."""
    result = await db.execute(
        select(SensorReadingsModel)
        .filter(SensorReadingsModel.sensor_id == sensorid)
        .filter(SensorReadingsModel.timestamp.between(start_date, end_date))
    )
    readings = result.scalars().all()

    response = [
        SensorReadings(
            datetime=reading.timestamp,
            temperature=reading.temperature,
            dissolved_oxygen=reading.dissolved_oxygen,
            dissolved_oxygen_percent=do_saturation_percent(reading.temperature, reading.dissolved_oxygen),
        )
        for reading in readings
    ]
    return SensorReadingsResponse(readings=response)


@router.get("/{sensorid}/readings/latest")
async def get_sensor_readings_latest_by_id(
    logged_in_user: get_logged_in_user_depends,
    sensorid: str,
    db: AsyncSession = Depends(get_db),
) -> SensorStatus:
    """Get latest sensor readings by ID."""
    result = await db.execute(
        select(SensorReadingsModel)
        .filter(SensorReadingsModel.sensor_id == sensorid)
        .order_by(SensorReadingsModel.timestamp.desc())
        .limit(1)
    )
    latest_reading = result.scalar()
    if not latest_reading:
        return None

    return SensorStatus(
        id=sensorid,
        name="Unknown",  # Fetch sensor name if needed
        datetime=latest_reading.timestamp,
        temperature=latest_reading.temperature,
        dissolved_oxygen=latest_reading.dissolved_oxygen,
        dissolved_oxygen_percent=do_saturation_percent(latest_reading.temperature, latest_reading.dissolved_oxygen),
    )


@router.get("/list")
async def get_sensor_ids(db: AsyncSession = Depends(get_db)) -> SensorListResponse:
    """Get all sensor IDs."""
    result = await db.execute(select(Sensors))
    sensors = result.scalars().all()

    response = [{"id": sensor.id, "name": sensor.name} for sensor in sensors]
    return SensorListResponse(sensors=response)
