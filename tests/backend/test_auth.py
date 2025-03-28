import pytest
from httpx import AsyncClient
from secrets import token_hex

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(base_url="http://localhost:8000/api/v1") as ac:
        name = f"{token_hex(16)}"
        password = f"{token_hex(16)}"

        response = await ac.post("/auth/register", json={
            "username": name,
            "email": f"{name}@test.com",
            "password": password
        })
        assert response.status_code == 200
        assert response.json()["success"]

        response = await ac.post("/auth/login", json={
            "username": name,
            "password": password
        })
        assert response.status_code == 200
        assert response.json()["success"]