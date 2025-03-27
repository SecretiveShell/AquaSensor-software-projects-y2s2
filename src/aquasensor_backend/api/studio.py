import asyncio
from datetime import datetime
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal
from typing import Any

from fastapi import APIRouter
from httpx import AsyncClient
from loguru import logger
from shapely.geometry import Point
from sqlalchemy import Select

from aquasensor_backend.api.utils import normalize_date
from aquasensor_backend.cache import cache
from aquasensor_backend.ORM import AsyncSessionLocal, SensorReadings, Sensors
from aquasensor_backend.security import get_logged_in_user_depends

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
        ttl=60 * 60,  # 1 hour
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


async def get_sensors(
    x1: float, y1: float, x2: float, y2: float, date: datetime | None = None
):
    """Get sensors from the database."""
    output = []

    async with AsyncSessionLocal() as session:
        sensorsq: Any = await session.execute(
            Select(Sensors)
            .where(Sensors.latitude >= x1)
            .where(Sensors.longitude >= y1)
            .where(Sensors.latitude <= x2)
            .where(Sensors.longitude <= y2)
        )
        sensors = sensorsq.scalars().all()

        for sensor in sensors:
            if date:
                readingq: Any = await session.execute(
                    Select(SensorReadings)
                    .where(SensorReadings.sensor_id == sensor.id)
                    .where(SensorReadings.timestamp <= date)
                    .order_by(SensorReadings.timestamp.desc())
                    .limit(1)
                )
                reading = readingq.scalars().first()

            else:
                readingq: Any = await session.execute(
                    Select(SensorReadings)
                    .where(SensorReadings.sensor_id == sensor.id)
                    .order_by(SensorReadings.timestamp.desc())
                    .limit(1)
                )
                reading = readingq.scalars().first()

            if reading is None:
                continue

            output.append(
                {
                    "id": sensor.id,
                    "latitude": sensor.latitude,
                    "longitude": sensor.longitude,
                    "name": sensor.name,
                    "temperature": reading.temperature,
                    "dissolved_oxygen": reading.dissolved_oxygen,
                    "timestamp": reading.timestamp,
                }
            )

    return output


def enrich_geometry_nodes_with_sensors(
    river_elements: list, sensors: list, max_distance: float = 0.01
):
    """Attach sensor data to the closest node (lat/lon) in river geometries."""

    # Preprocess sensors as Points
    sensor_points = [
        (
            Point(sensor["longitude"], sensor["latitude"]),
            sensor,
        )
        for sensor in sensors
    ]

    for element in river_elements:
        if element["type"] != "way" or "geometry" not in element:
            continue

        geometry = element["geometry"]

        # Convert geometry to Points
        node_points = [
            (i, Point(node["lon"], node["lat"])) for i, node in enumerate(geometry)
        ]

        # Track which sensor is closest to which node
        for spoint, sensor in sensor_points:
            closest_index = None
            min_dist = float("inf")

            for i, node_point in node_points:
                dist = spoint.distance(node_point)
                if dist < min_dist:
                    min_dist = dist
                    closest_index = i

            if closest_index is not None and min_dist <= max_distance:
                node = geometry[closest_index]
                # Only attach if not already present (or prefer latest timestamp)
                if (
                    "sensor_timestamp" not in node
                    or sensor["timestamp"].isoformat() > node["sensor_timestamp"]
                ):
                    node["sensor_temperature"] = f"{sensor['temperature']:.2f}"
                    node["sensor_dissolved_oxygen"] = (
                        f"{sensor['dissolved_oxygen']:.2f}"
                    )
                    node["sensor_timestamp"] = sensor["timestamp"].isoformat()
                    node["sensor_id"] = sensor["id"]
                    node["sensor_name"] = sensor["name"]

    return river_elements


@router.get("/riverpoints")
async def get_river_points(
    logged_in_user: get_logged_in_user_depends,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    date: datetime | None = None,
):
    """Get river data for a given area."""

    if date:
        date = normalize_date(date)

    # normalize the bbox and make x1/y1 the smallest value
    x1, y1, x2, y2 = normalize_bbox(x1, y1, x2, y2)

    # get river data
    river_data, sensors = await asyncio.gather(
        get_river_points_overpass_cached(x1, y1, x2, y2),
        get_sensors(x1, y1, x2, y2, date),
    )

    # enrich river data with sensor data
    enriched = enrich_geometry_nodes_with_sensors(
        river_data.get("elements", []), sensors
    )

    # return enriched river data
    return {
        "version": 0.6,
        "generator": "aquasensor-backend",
        "elements": enriched,
    }
