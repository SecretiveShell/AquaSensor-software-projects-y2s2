from datetime import datetime
from fastapi import FastAPI
from api_middleware.downstream_auth import auth_required
from api_middleware.models import (
    HealthCheckResponse,
    SensorListResponse,
    SensorStatus,
    SensorStatusResponse,
    SensorReadingsResponse,
)
from api_middleware.functions import get_status, get_status_by_id, get_sensor_ids as get_sensor_ids_function
from api_middleware.historical import get_historical_data

app = FastAPI(
    title="API Middleware",
    description="API for retrieving sensor status and readings from AquaSensor.",
)


@app.get("/health")
async def get_health() -> HealthCheckResponse:
    """Health check endpoint."""
    return HealthCheckResponse(status="OK")


@app.get("/status", dependencies=[auth_required])
async def get_sensor_status() -> SensorStatusResponse:
    """Get sensor status."""

    return await get_status()


@app.get("/sensors/{sensorid}/status", dependencies=[auth_required])
async def get_sensor_status_by_id(sensorid: str) -> SensorStatus:
    """Get sensor status by ID."""

    return await get_status_by_id(sensorid)


@app.get("/sensors/{sensorid}/readings", dependencies=[auth_required])
async def get_sensor_readings_by_id(
    sensorid: str, start_date: datetime, end_date: datetime
) -> SensorReadingsResponse:
    """Get sensor readings by ID."""

    return await get_historical_data(sensorid, start_date, end_date)


@app.get("/sensors/{sensorid}/readings/latest", dependencies=[auth_required])
async def get_sensor_readings_latest_by_id(sensorid: str) -> SensorStatus:
    """Get latest sensor readings by ID."""

    return await get_status_by_id(sensorid)

@app.get("/sensors/list", dependencies=[auth_required])
async def get_sensor_ids() -> SensorListResponse:
    """Get all sensor ids."""

    return await get_sensor_ids_function()