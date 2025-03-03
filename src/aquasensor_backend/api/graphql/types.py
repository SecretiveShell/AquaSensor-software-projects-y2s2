from datetime import datetime, timezone
import strawberry
from typing import Optional


def current_utc_datetime() -> datetime:
    """Returns the current UTC datetime."""
    return datetime.now(timezone.utc)


@strawberry.type
class Sensor:
    """Represents a sensor's metadata."""
    id: str
    name: str


@strawberry.type
class SensorStatus:
    """Represents real-time status of a sensor."""
    id: str
    name: str
    timestamp: datetime
    temperature: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    oxygen_saturation: Optional[float] = None


@strawberry.type
class SensorReading:
    """Represents a single sensor data point."""
    timestamp: datetime
    temperature: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    oxygen_saturation: Optional[float] = None


@strawberry.input
class SensorReadingsFilter:
    """Filter for retrieving sensor readings within a time range."""
    start_time: datetime = strawberry.field(default_factory=current_utc_datetime)
    end_time: datetime = strawberry.field(default_factory=current_utc_datetime)


@strawberry.input
class Credentials:
    """User login credentials."""
    username: str
    password: str


@strawberry.type
class AuthResponse:
    """Response for authentication-related queries."""
    success: bool
    token: Optional[str] = None
    message: Optional[str] = None


@strawberry.input
class Registration:
    """New user registration data."""
    username: str
    email: str
    password: str


@strawberry.type
class User:
    """Represents a user profile."""
    username: str
    email: str


@strawberry.type
class LogoutResponse:
    """Represents the result of a logout operation."""
    success: bool
