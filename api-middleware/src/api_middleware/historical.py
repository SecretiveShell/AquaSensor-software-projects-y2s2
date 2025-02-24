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
        istream = response.aiter_text(1)
        for i in range(35):
             _ = await anext(istream)
        dt=[]
        temperature=[]
        dissolved_oxygen=[]
        percentage=[]
        #begin stream process
        while(None!=(buffer:=[await anext(istream,None)])[0]):
            #datetime (left in aquasensor format in hopes they change it)
            for i in range(7):
                buffer+=[await anext(istream)]
            _=await anext(istream)
            buffer+=["T"]
            for i in range(8):
                buffer+=[await anext(istream)]
            dt+=[''.join(buffer)]
            _=await anext(istream)

            #temperature
            buffer=[]
            cbuffer=await anext(istream)
            if cbuffer!='N':
                buffer+=[cbuffer]
                while(','!=(cbuffer:=await anext(istream))):
                    buffer+=[cbuffer]
                temperature+=[float(''.join(buffer))]
            else:
                temperature+=[0]
                _=await anext(istream)
                _=await anext(istream)
                _=await anext(istream)

            #dissolved oxygen
            buffer=[]
            cbuffer=await anext(istream)
            if cbuffer!='N':
                buffer+=[cbuffer]
                while(','!=(cbuffer:=await anext(istream))):
                    buffer+=[cbuffer]
                dissolved_oxygen+=[float(''.join(buffer))]
            else:
                dissolved_oxygen+=[0]
                _=await anext(istream)
                _=await anext(istream)
                _=await anext(istream)
            
            #dissolved oxygen
            buffer=[]
            cbuffer=await anext(istream)
            if cbuffer!='N':
                buffer=+[cbuffer]
                while('\n'!=(cbuffer:=await anext(istream))):
                    buffer+=[cbuffer]
                percentage+=[float(''.join(buffer))]
            else:
                percentage+=[0]
                _=await anext(istream)
                _=await anext(istream)
                _=await anext(istream)

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
