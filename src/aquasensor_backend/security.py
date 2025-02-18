"""all security related functions"""

from hashlib import blake2b
from os import getenv

from fastapi.security import APIKeyHeader
from loguru import logger
from typing import Annotated
from fastapi import Depends, HTTPException

from aquasensor_backend.cache import cache
from aquasensor_backend.models.auth import UserModel

# salt used for hashing passwords. must be a constant
PASSWORD_SALT = getenv("PASSWORD_SALT") or "AQUASENSOR"

if PASSWORD_SALT == "AQUASENSOR":
    logger.warning("PASSWORD_SALT is not set. Using default value. Please set PASSWORD_SALT environment variable.")


def hash_password(password: str) -> str:
    """hash a password"""

    return blake2b(password.encode("utf-8"), digest_size=64, salt=PASSWORD_SALT.encode("utf-8")).hexdigest()


api_key_header = APIKeyHeader(name="AquaSensor-Login-Token")

async def get_logged_in_user(token: Annotated[str, Depends(api_key_header)]):
    """check if the user is logged in"""

    cached_user = await cache.get(token)
    if cached_user is None:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        user = UserModel.model_validate(cached_user)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user

get_logged_in_user_depends = Annotated[UserModel, Depends(get_logged_in_user)]
