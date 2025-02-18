from contextlib import asynccontextmanager
from fastapi import FastAPI

from aquasensor_backend.ORM import init_db
from loguru import logger

@asynccontextmanager
async def lifespan(app: FastAPI):
    try: 
        await init_db()
    except Exception:
        logger.warning("failed to initialize database, is the database down?.")
    
    yield