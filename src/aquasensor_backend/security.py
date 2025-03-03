"""all security related functions."""

from datetime import timedelta
from secrets import token_hex
from argon2 import PasswordHasher

from fastapi.security import APIKeyHeader
from typing import Annotated
from fastapi import Depends, HTTPException

from aquasensor_backend.cache import cache
from aquasensor_backend.models.auth import UserModel

AUTH_TOKEN_TTL = timedelta(days=1).total_seconds()

def hash_password(password: str) -> str:
    """hash a password"""

    # argon 2 password hash
    password_hasher = PasswordHasher()
    hashed_password = password_hasher.hash(password)
    return hashed_password


api_key_header = APIKeyHeader(name="AquaSensor-Login-Token")

CACHE_TOKEN_KEY_PREFIX = "session-token:"

async def create_login_session(username: str, email: str):
    user = UserModel(username=username, email=email) 
    token = token_hex(128)

    await cache.set(CACHE_TOKEN_KEY_PREFIX + token, user, ttl=AUTH_TOKEN_TTL)

    return token

async def fapi_get_user(token: Annotated[str, Depends(api_key_header)]):
    """check if the user is logged in"""

    return get_logged_in_user(token)

async def get_logged_in_user(token):
    """check if the user is logged in"""

    cached_user = await cache.get(CACHE_TOKEN_KEY_PREFIX + token)
    if cached_user is None:
        raise HTTPException(status_code=401, detail="Invalid API key")

    try:
        user = UserModel.model_validate(cached_user)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return user


get_logged_in_user_depends = Annotated[UserModel, Depends(fapi_get_user)]
