from datetime import datetime, timezone
import strawberry
from strawberry.permission import PermissionExtension
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
        return AuthResponse(success=True, token="mock_token")

    @strawberry.field
    async def register(self, registration: Registration) -> AuthResponse:
        """Registers a new user and returns a token."""
        return AuthResponse(success=True, token="mock_token")

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def logout(self, token: str) -> LogoutResponse:
        """Logs out a user and invalidates their session."""
        return LogoutResponse(success=True)

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def sensors(self) -> List[Sensor]:
        """Retrieves all available sensors."""
        return [
            Sensor(id="1", name="Temperature Sensor"),
            Sensor(id="2", name="Oxygen Sensor")
        ]

    @strawberry.field(extensions=[PermissionExtension(permissions=[IsAuthenticated()])])
    async def sensor_status(self, sensor_id: str) -> Optional[SensorStatus]:
        """Fetches the real-time status of a specified sensor."""
        return SensorStatus(
            id=sensor_id,
            name=f"Sensor {sensor_id}",
            timestamp=current_utc_datetime(),
            temperature=25.0,
            dissolved_oxygen=0.5,
            oxygen_saturation=50.0
        )

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
