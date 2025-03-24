from fastapi import APIRouter

from .auth import router as auth_router
from .sensors import router as sensors_router
from .studio import router as studio_router
from .graphql import graphql_app as graphql_app

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(sensors_router, prefix="/sensors", tags=["sensors"])
router.include_router(studio_router, prefix="/studio", tags=["studio"])
router.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

@router.get("/graphql-schema")
async def graphql_schema():
    """Return the GraphQL schema for the API."""
    return str(graphql_app.schema.as_str())