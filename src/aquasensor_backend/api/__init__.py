from fastapi import APIRouter

from .auth import router as auth_router
from .sensors import router as sensors_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(sensors_router, prefix="/sensors", tags=["sensors"])
