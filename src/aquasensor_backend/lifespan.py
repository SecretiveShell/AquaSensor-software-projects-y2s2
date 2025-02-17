from contextlib import asynccontextmanager
from fastapi import FastAPI

from aquasensor_backend.ORM import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield