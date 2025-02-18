from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
import os

# pull the api key from env vars
# this would be set via a secret manager like hashicorp vault
valid_api_key = os.environ.get("MIDDLEWARE_API_KEY")
assert valid_api_key, "MIDDLEWARE_API_KEY environment variable is not set."


def get_api_key(api_key: str = APIKeyHeader(...)):
    """Validate API key."""

    if api_key != valid_api_key:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


auth_required = Depends(get_api_key)
