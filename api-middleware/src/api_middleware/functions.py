from aiocache import cached
from fastapi import HTTPException
from httpx import AsyncClient as Client
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlencode
from datetime import datetime
from os import getenv

BASE_URL = r"https://api.aquasensor.co.uk/aq.php"
USERNAME = getenv("AQUASENSOR_USERNAME")
TOKEN = getenv("AQUASENSOR_TOKEN")

assert USERNAME, "AQUASENSOR_USERNAME environment variable is not set."
assert TOKEN, "AQUASENSOR_TOKEN environment variable is not set."


async def get_status() -> dict:
    url = urlparse(BASE_URL)
    params = urlencode({"op": "status", "username": USERNAME, "token": TOKEN})
    url = url.geturl() + f"?{params}"

    async with Client() as client:
        response = await client.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")

    # Extract rows
    rows = table.find_all("tr")

    # Extract headers
    headers = [header.get_text(strip=True) for header in rows[0].find_all("td")]

    # convert some headers to our json format
    headers[0] = "id"
    headers[1] = "name"
    headers[2] = "datetime"
    headers[3] = "temperature"
    headers[4] = "dissolved_oxygen"
    headers[5] = "dissolved_oxygen_percent"

    # Extract data
    parsed_data = []
    for row in rows[1:]:
        values = [cell.get_text(strip=True) for cell in row.find_all("td")]
        data = dict(zip(headers, values))
        data["datetime"] = datetime.strptime(data["datetime"], r"%d/%m/%y %H:%M")
        data["dissolved_oxygen"] = float(
            data["dissolved_oxygen"].removesuffix(" mg/L").strip()
        )
        data["dissolved_oxygen_percent"] = float(
            data["dissolved_oxygen_percent"].removesuffix("%").strip()
        )
        parsed_data.append(data)

    return {"sensors": parsed_data}


async def get_status_by_id(sensorid: str) -> dict:
    status = await get_status()
    sensors = status["sensors"]
    for sensor in sensors:
        if sensor["id"] == sensorid:
            return sensor

    raise HTTPException(status_code=404, detail="Sensor not found")

@cached()
async def get_sensor_ids() -> list:
    status = await get_status()
    sensors = status["sensors"]
    return [
        {"id": sensor["id"], "name": sensor["name"]} for sensor in sensors
    ]