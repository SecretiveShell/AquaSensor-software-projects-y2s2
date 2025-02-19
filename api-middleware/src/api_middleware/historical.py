from datetime import datetime
from math import isnan
from fastapi import HTTPException
from httpx import AsyncClient as Client
from api_middleware.functions import BASE_URL, USERNAME, TOKEN


async def get_historical_data(
    sensorid: str, start_date: datetime, end_date: datetime
) -> dict:
    start = f"{start_date.strftime('%d-%m')}-{start_date.strftime('%y')[:2]}"
    end = f"{end_date.strftime('%d-%m')}-{end_date.strftime('%y')[:2]}"

    url = (
        f"{BASE_URL}?op=readings&sensorid={sensorid}&username={USERNAME}&token={TOKEN}"
    )
    url += f"&fromdate={start}&todate={end}"

    print(url)

    async with Client() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to retrieve historical data",
        )

    raw_data = response.text
    data = raw_data.split("\n")
    data = data[1:]

    readings = []
    for row in data:
        if row == "":
            continue

        row = row.split(",")

        for i in range(len(row)):
            row[i] = row[i].strip()

        dt = datetime.strptime(f"{row[0]} {row[1]}", r"%d-%m-%y %H:%M:%S")

        temperature = row[2] if row[2] and not isnan(float(row[2])) else None
        dissolved_oxygen = row[3] if row[3] and not isnan(float(row[3])) else None
        dissolved_oxygen_percent = (
            row[4] if row[4] and not isnan(float(row[4])) else None
        )

        readings.append(
            {
                "datetime": dt,
                "temperature": temperature,
                "dissolved_oxygen": dissolved_oxygen,
                "dissolved_oxygen_percent": dissolved_oxygen_percent,
            }
        )

    return {"readings": readings}
