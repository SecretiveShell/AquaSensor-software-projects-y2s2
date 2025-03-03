from datetime import datetime
from fastapi import APIRouter
from aquasensor_backend.security import get_logged_in_user_depends
from aquasensor_backend.models.sensor import (
    SensorListResponse,
    SensorStatus,
    SensorStatusResponse,
    SensorReadingsResponse,
)
from httpx import AsyncClient as Client
from aquasensor_backend.config import API_BASE_URL, API_API_KEY

router = APIRouter()


@router.get("/status")
async def get_sensor_status(
    logged_in_user: get_logged_in_user_depends,
) -> SensorStatusResponse:
    """Get sensor status."""

    async with Client(headers={"api-key": API_API_KEY}) as client:
        response = await client.get(API_BASE_URL + "/status")

    return response.json()


@router.get("/sensors/{sensorid}/status")
async def get_sensor_status_by_id(
    logged_in_user: get_logged_in_user_depends, sensorid: str
) -> SensorStatus:
    """Get sensor status by ID."""

    async with Client(headers={"api-key": API_API_KEY}) as client:
        response = await client.get(API_BASE_URL + f"/sensors/{sensorid}/status")

    return response.json()


@router.get("/sensors/{sensorid}/readings")
async def get_sensor_readings_by_id(
    logged_in_user: get_logged_in_user_depends,
    sensorid: str,
    start_date: datetime,
    end_date: datetime,
) -> SensorReadingsResponse:
    """Get sensor readings by ID."""

    async with Client(headers={"api-key": API_API_KEY}) as client:
        response = await client.get(API_BASE_URL + f"/sensors/{sensorid}/readings", params={"start_date": start_date, "end_date": end_date})

    return response.json()


@router.get("/sensors/{sensorid}/readings/latest")
async def get_sensor_readings_latest_by_id(
    logged_in_user: get_logged_in_user_depends, sensorid: str
) -> SensorStatus:
    """Get latest sensor readings by ID."""

    async with Client(headers={"api-key": API_API_KEY}) as client:
        response = await client.get(
            API_BASE_URL + f"/sensors/{sensorid}/readings/latest"
        )

    return response.json()

@router.get("/list")
async def get_sensor_ids() -> SensorListResponse:
    """Get all sensor ids."""

    async with Client(headers={"api-key": API_API_KEY}) as client:
        response = await client.get(API_BASE_URL + "/sensors/list")

    return response.json()