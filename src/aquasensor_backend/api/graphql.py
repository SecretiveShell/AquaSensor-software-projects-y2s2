from datetime import datetime, timezone
from fastapi import Depends
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional
from httpx import AsyncClient as Client

from aquasensor_backend.security import get_logged_in_user_depends
from aquasensor_backend.config import API_BASE_URL, API_API_KEY
from functools import partial

# Utility function to always return the current UTC datetime
current_utc_datetime = partial(datetime.now, timezone.utc)

# ------------------- GraphQL Types -------------------

@strawberry.type
class Sensor:
    """GraphQL type for a sensor metadata."""
    id: str
    name: str


@strawberry.type
class SensorStatus:
    """GraphQL type for real-time sensor status."""
    id: str
    name: str
    datetime: datetime
    temperature: Optional[str] = None
    dissolved_oxygen: Optional[float] = None
    dissolved_oxygen_percent: Optional[float] = None


@strawberry.type
class SensorReading:
    """GraphQL type for a single sensor reading."""
    datetime: datetime
    temperature: Optional[float] = None
    dissolved_oxygen: Optional[float] = None
    dissolved_oxygen_percent: Optional[float] = None


@strawberry.input
class SensorReadingsFilter:
    """GraphQL input type for filtering sensor readings."""
    from_date: datetime = strawberry.field(default_factory=current_utc_datetime)
    to_date: datetime = strawberry.field(default_factory=current_utc_datetime)

# ------------------- Helper Functions -------------------

async def fetch_api_data(endpoint: str, params: dict = None):
    """Helper function to fetch data from the API."""
    async with Client(headers={"api-key": API_API_KEY}) as client:
        response = await client.get(API_BASE_URL + endpoint, params=params)
    return response.json()

# ------------------- GraphQL Queries -------------------

@strawberry.type
class Query:
    @strawberry.field
    async def sensors(self) -> List[Sensor]:
        """Fetch all sensors (IDs and names)."""
        data = await fetch_api_data("/sensors/list")
        return [Sensor(**sensor) for sensor in data["sensors"]]

    @strawberry.field
    async def sensor_status(
        self, sensorid: str, logged_in_user: str = Depends(get_logged_in_user_depends)
    ) -> SensorStatus:
        """Fetch the status of a single sensor by ID."""
        data = await fetch_api_data(f"/sensors/{sensorid}/status")
        return SensorStatus(**data)

    @strawberry.field
    async def latest_sensor_reading(
        self, sensorid: str, logged_in_user: str = Depends(get_logged_in_user_depends)
    ) -> Optional[SensorReading]:
        """Fetch the latest reading for a given sensor ID."""
        data = await fetch_api_data(f"/sensors/{sensorid}/readings/latest")

        if not data or "datetime" not in data:
            return None  # Handle empty or invalid API response

        # Extract only the required fields
        return SensorReading(
            datetime=data["datetime"],
            temperature=data.get("temperature"),
            dissolved_oxygen=data.get("dissolved_oxygen"),
            dissolved_oxygen_percent=data.get("dissolved_oxygen_percent"),
        )

    @strawberry.field
    async def sensor_readings(
        self,
        sensorid: str,
        filter: SensorReadingsFilter,
        logged_in_user: str = Depends(get_logged_in_user_depends),
    ) -> List[SensorReading]:
        """Fetch sensor readings for a given sensor ID in a date range."""
        params = {"fromdate": filter.from_date, "todate": filter.to_date}
        data = await fetch_api_data(f"/sensors/{sensorid}/readings", params=params)

        if not data or "readings" not in data:
            return []  # Return empty list if API response is missing 'readings'

        # Extract valid readings only
        return [
            SensorReading(
                datetime=reading["datetime"],
                temperature=reading.get("temperature"),
                dissolved_oxygen=reading.get("dissolved_oxygen"),
                dissolved_oxygen_percent=reading.get("dissolved_oxygen_percent"),
            )
            for reading in data["readings"]
        ]



# ------------------- GraphQL Schema -------------------

schema = strawberry.Schema(query=Query)

# Create GraphQL router
graphql_app = GraphQLRouter(schema)
