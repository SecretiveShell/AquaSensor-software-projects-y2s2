import pytest
from httpx import AsyncClient
from redis import Redis
from secrets import token_hex

API_KEY = token_hex(128)
HEADERS = {"Aquasensor-Login-Token": f"{API_KEY}"}

r = Redis.from_url("redis://localhost:6379")
r.set(name=f"session-token:{API_KEY}", value="{\"username\":\"test\",\"email\":\"test@testers.com\"}")

@pytest.mark.asyncio
async def test_sensor_list():
    async with AsyncClient(base_url="http://localhost:8000/api/v1") as ac:
        response = await ac.get("/sensors/list", headers=HEADERS)
        assert response.status_code == 200
        assert "sensors" in response.json()

@pytest.mark.asyncio
async def test_sensor_status():
    async with AsyncClient(base_url="http://localhost:8000/api/v1") as ac:
        list_response = await ac.get("/sensors/list", headers=HEADERS)
        sensors = list_response.json().get("sensors", [])
        if sensors:
            sensor_id = sensors[0]["id"]
            status_response = await ac.get(f"/sensors/{sensor_id}/status", headers=HEADERS)
            assert status_response.status_code == 200