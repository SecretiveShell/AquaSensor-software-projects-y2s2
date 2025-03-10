from fastapi import APIRouter

from .auth import router as auth_router
from .graphql import graphql_app as graphql_app

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(graphql_app, prefix="/graphql", tags=["graphql"])

@router.get("/graphql-schema")
async def graphql_schema():
    """Return the GraphQL schema for the API."""
    return str(graphql_app.schema.as_str())