from datetime import datetime, timezone
import httpx
import strawberry
from strawberry.permission import PermissionExtension
from loguru import logger

from aquasensor_backend.config import API_API_KEY, API_BASE_URL
from aquasensor_backend.security import create_login_session, create_user_account, validate_username_password
from .types import (
    AuthResponse,
    Credentials,
    LogoutResponse,
    Registration,
    Sensor,
    SensorReading,
    SensorReadingsFilter,
    SensorStatus,
    User
)
from .permissions import IsAuthenticated
from typing import List, Optional

def current_utc_datetime() -> datetime:
    """Returns the current UTC datetime."""
    return datetime.now(timezone.utc)

@strawberry.type
class Query:
    """GraphQL query operations."""

    @strawberry.field
    async def login(self, credentials: Credentials) -> AuthResponse:
        """Authenticates a user and returns a token."""

        try:
            valid, message, email = await validate_username_password(credentials.username, credentials.password)
            if valid:
                token = await create_login_session(credentials.username, email)
                return AuthResponse(success=True, token=token)
            else:
                return AuthResponse(success=False, message=message)
        except Exception as e:
            logger.error(e)
            return AuthResponse(success=False, message="Invalid username or password.")

    @strawberry.field
    async def register(self, registration: Registration) -> AuthResponse:
        """Registers a new user and returns a token."""
        success = await create_user_account(registration.username, registration.email, registration.password)

        if not success:
            return AuthResponse(success=False, message="Account already exists.")

        token = await create_login_session(registration.username, registration.email)

        return AuthResponse(success=True, token=token)

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def logout(self, token: str) -> LogoutResponse:
        """Logs out a user and invalidates their session."""
        return LogoutResponse(success=True)

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def sensors(self) -> List[Sensor]:
        """Retrieves all available sensors."""
        async with httpx.AsyncClient(headers={"api-key": API_API_KEY}) as client:
            response = await client.get(f"{API_BASE_URL}/sensors/list")
            data = response.json()

        return [Sensor(**sensor) for sensor in data["sensors"]]

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def sensor_status(self, sensor_id: str) -> Optional[SensorStatus]:
        """Fetches the real-time status of a specified sensor."""
        async with httpx.AsyncClient(headers={"api-key": API_API_KEY}) as client:
            response = await client.get(f"{API_BASE_URL}/sensors/{sensor_id}/status")
            data: dict = response.json()

        data["timestamp"] = data.pop("datetime")
        data["oxygen_saturation"] = data.pop("dissolved_oxygen_percent")

        return SensorStatus(**data)

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def latest_sensor_reading(self, sensor_id: str) -> Optional[SensorReading]:
        """Retrieves the most recent reading from a specified sensor."""
        return SensorReading(
            timestamp=current_utc_datetime(),
            temperature=25.0,
            dissolved_oxygen=0.5,
            oxygen_saturation=50.0
        )

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def sensor_readings(self, sensor_id: str, filter: SensorReadingsFilter) -> List[SensorReading]:
        """Fetches sensor readings within a specified date range."""
        return [
            SensorReading(
                timestamp=current_utc_datetime(),
                temperature=25.0,
                dissolved_oxygen=0.5,
                oxygen_saturation=50.0
            )
        ]

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def user(self, token: str) -> Optional[User]:
        """Retrieves user details for the given authentication token."""
        return User(username="mock_user", email="user@example.com")
