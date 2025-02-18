"""all security related functions."""

from argon2 import PasswordHasher
from os import getenv

from fastapi.security import APIKeyHeader
from loguru import logger
from typing import Annotated
from fastapi import Depends, HTTPException

from aquasensor_backend.cache import cache
from aquasensor_backend.models.auth import UserModel


def hash_password(password: str) -> str:
    """hash a password"""

    # Using sha3_256 for hashing instead of blake2b
    p=PasswordHasher()
    h=p.hash(password)
    return h


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
