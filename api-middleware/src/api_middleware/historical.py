from datetime import datetime
from math import isnan
from fastapi import HTTPException
from httpx import AsyncClient as Client
from api_middleware.functions import BASE_URL, USERNAME, TOKEN
from aiocache import cached

@cached(ttl=60) # TODO: make this redis?
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

    async with Client().stream(method="GET",url=url) as response:
        if response.status_code != 200:
            raise HTTPException(
                    status_code=response.status_code,
                    detail="Failed to retrieve data"
                )
        istream = response.aiter_bytes(1)
        for i in range(35):
            await _ = next(istream)
        dt=[]
        temperature=[]
        dissolved_oxygen=[]
        percentage=[]
        #begin stream process
        while(None!=(buffer:=[next(istream,None)])[0]):
            #datetime (left in aquasensor format in hopes they change it)
            for i in range(7):
                await buffer+=[next(istream)]
            await _=next(istream)
            buffer+=["T"]
            for i in range(8):
                await buffer+=[next(istream)]
            dt+=[''.join(buffer)]
            await _=next(istream)

            #temperature
            buffer=[]
            await while(','!=(cbuffer:=next(istream))):
                buffer+=[cbuffer]
            temperature+=[''.join(buffer)]

            #dissolved oxygen
            buffer=[]
            await while(','!=(cbuffer:=next(istream))):
                buffer+=[cbuffer]
            dissolved_oxygen+=[''.join(buffer)]
            
            #dissolved oxygen
            buffer=[]
            await while('\n'!=(cbuffer:=next(istream))):
                buffer+=[cbuffer]
            percentage+=[''.join(buffer)]
        #end stream process 
  
   

    readings = []
    readings.append(
        {
            "datetime": dt,
            "temperature": temperature,
            "dissolved_oxygen": dissolved_oxygen,
            "dissolved_oxygen_percent": percentage,
        }
    )

    return {"readings": readings}
