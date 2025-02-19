from datetime import datetime
from fastapi import APIRouter
from aquasensor_backend.security import get_logged_in_user_depends
from aquasensor_backend.models.sensor import (
    SensorStatus,
    SensorStatusResponse,
    SensorReadingsResponse,
)
from httpx import AsyncClient as Client
from os import getenv

API_BASE_URL = getenv("API_BASE_URL")
assert API_BASE_URL, "API_BASE_URL environment variable is not set."

API_API_KEY = getenv("API_API_KEY")
assert API_API_KEY, "API_API_KEY environment variable is not set."

router = APIRouter()

@router.get("/status")
async def get_sensor_status(logged_in_user: get_logged_in_user_depends) -> SensorStatusResponse:
    """Get sensor status."""

    return {}


@router.get("/sensors/{sensorid}/status")
async def get_sensor_status_by_id(logged_in_user: get_logged_in_user_depends, sensorid: str) -> SensorStatus:
    """Get sensor status by ID."""

    return {}


@router.get("/sensors/{sensorid}/readings")
async def get_sensor_readings_by_id(
    logged_in_user: get_logged_in_user_depends, sensorid: str, start_date: datetime, end_date: datetime
) -> SensorReadingsResponse:
    """Get sensor readings by ID."""

    return {}


@router.get("/sensors/{sensorid}/readings/latest")
async def get_sensor_readings_latest_by_id(logged_in_user: get_logged_in_user_depends, sensorid: str) -> SensorStatus:
    """Get latest sensor readings by ID."""

    return {}
