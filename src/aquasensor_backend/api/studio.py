from datetime import datetime
from typing import Any
from fastapi import APIRouter
from httpx import AsyncClient
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING

from loguru import logger
from sqlalchemy import Select

from aquasensor_backend.cache import cache
from aquasensor_backend.ORM import Sensors, SensorReadings, AsyncSessionLocal

router = APIRouter()


def to_decimal(value: float, places: int, rounding: str):
    d = Decimal(str(value))
    return float(d.quantize(Decimal(f"1e-{places}"), rounding=rounding))


def normalize_bbox(x1, y1, x2, y2, precision=1):
    x_min = to_decimal(min(x1, x2), precision, ROUND_FLOOR)
    y_min = to_decimal(min(y1, y2), precision, ROUND_FLOOR)
    x_max = to_decimal(max(x1, x2), precision, ROUND_CEILING)
    y_max = to_decimal(max(y1, y2), precision, ROUND_CEILING)

    return (x_min, y_min, x_max, y_max)

async def get_river_points_overpass_cached(x1: float, y1: float, x2: float, y2: float):
    key = f"river-points:{x1}_{y1}_{x2}_{y2}"

    result = await cache.get(key)
    if result is not None:
        return result

    result = await get_river_points_overpass(x1, y1, x2, y2)
    await cache.set(
        key=key, 
        value=result, 
        ttl=60 * 60 # 1 hour
    )

    return result

async def get_river_points_overpass(x1: float, y1: float, x2: float, y2: float):
    """Get river geometry data from Overpass API."""

    logger.info(f"Fetching river data for bbox: {x1}, {y1}, {x2}, {y2}")

    north = max(x1, x2)
    south = min(x1, x2)
    east = max(y1, y2)
    west = min(y1, y2)

    overpass_query = f"""
        [out:json];
        way
          ["waterway"="river"]
          ({south},{west},{north},{east});
        out geom;
    """

    # url = "https://overpass-api.de/api/interpreter"
    url = "https://overpass.kumi.systems/api/interpreter?data="

    headers = {
        "User-Agent": "https://github.com/SecretiveShell/AquaSensor-software-projects-y2s2",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    async with AsyncClient(timeout=30.0) as client:
        response = await client.post(
            url, data={"data": overpass_query}, headers=headers
        )
        response.raise_for_status()
        data = response.json()

    return data

async def get_sensors(x1: float, y1: float, x2: float, y2: float):
    """Get sensors from the database."""
    output = []

    async with AsyncSessionLocal() as session:
        sensorsq: Any = await session.execute(
            Select(Sensors).where(Sensors.latitude >= x1).where(Sensors.longitude >= y1).where(Sensors.latitude <= x2).where(Sensors.longitude <= y2)
        )
        sensors = sensorsq.scalars().all()

        for sensor in sensors:
            readingq: Any = await session.execute(
                Select(SensorReadings).where(SensorReadings.sensor_id == sensor.id).order_by(SensorReadings.timestamp.desc()).limit(1)
            )
            reading = readingq.scalars().first()

            if reading is None:
                continue
            
            output.append({
                "id": sensor.id,
                "latitude": sensor.latitude,
                "longitude": sensor.longitude,
                "name": sensor.name,
                "temperature": reading.temperature,
                "dissolved_oxygen": reading.dissolved_oxygen,
                "timestamp": reading.timestamp,
            })
    
    return output


@router.get("/riverpoints")
async def get_river_points(
    x1: float, y1: float, x2: float, y2: float, date: datetime | None = None
):
    """Get river data for a given area."""

    # normalize the bbox and make x1/y1 the smallest value
    x1, y1, x2, y2 = normalize_bbox(x1, y1, x2, y2)

    # get data from overpass
    data = await get_river_points_overpass_cached(x1, y1, x2, y2)

    print(f"sensors: {await get_sensors(x1, y1, x2, y2)}")

    return data
