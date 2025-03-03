from pydantic import BaseModel, Field
from typing import List, Annotated
from datetime import datetime, timezone
from functools import partial


class HealthCheckResponse(BaseModel):
    """Response model for health check API."""

    status: Annotated[str, Field(description="Status of the API.")] = "OK"


class SensorStatus(BaseModel):
    """Model representing the current status of a sensor."""

    id: Annotated[str, Field(description="Unique sensor identifier.")]
    name: Annotated[str, Field(description="Name or location of the sensor.")]
    datetime: Annotated[
        datetime, Field(description="Timestamp of the latest reading (ISO 8601).")
    ]
    temperature: Annotated[
        float | None,
        Field(description="Temperature recorded by the sensor (e.g., '5.12C')."),
    ]
    dissolved_oxygen: Annotated[
        float | None, Field(description="Dissolved oxygen level in mg/L.")
    ]
    dissolved_oxygen_percent: Annotated[
        float | None,
        Field(
            description="Dissolved oxygen percentage relative to standard saturation."
        ),
    ]


class SensorReadings(BaseModel):
    """Model representing a single sensor reading entry."""

    datetime: Annotated[
        datetime, Field(description="Date and time of the reading (ISO 8601).")
    ]
    temperature: Annotated[
        float | None, Field(description="Temperature value recorded in Celsius.")
    ]
    dissolved_oxygen: Annotated[
        float | None, Field(description="Dissolved oxygen level in mg/L.")
    ]
    dissolved_oxygen_percent: Annotated[
        float | None, Field(description="Dissolved oxygen saturation percentage.")
    ]


class SensorStatusResponse(BaseModel):
    """Response model for sensor status API."""

    sensors: Annotated[
        List[SensorStatus],
        Field(description="List of sensors with their latest status."),
    ]


class SensorReadingsResponse(BaseModel):
    """Response model for sensor readings API."""

    readings: Annotated[
        List[SensorReadings],
        Field(description="List of recorded readings for a sensor."),
    ]


# Create a partial function to always return the current UTC datetime
current_utc_datetime = partial(datetime.now, timezone.utc)


class SensorReadingsRequest(BaseModel):
    """Query parameters for fetching sensor readings."""

    fromdate: Annotated[
        datetime,
        Field(
            default_factory=current_utc_datetime,
            description="Start datetime (ISO 8601) for filtering readings.",
        ),
    ]
    todate: Annotated[
        datetime,
        Field(
            default_factory=current_utc_datetime,
            description="End datetime (ISO 8601) for filtering readings.",
        ),
    ]

class Sensor(BaseModel):
    """Model representing a single sensor."""

    id: Annotated[str, Field(description="Unique sensor identifier.")]
    name: Annotated[str, Field(description="Name or location of the sensor.")]

class SensorListResponse(BaseModel):
    """Response model for sensor list API."""

    sensors: Annotated[
        List[Sensor],
        Field(description="List of sensors"),
    ]