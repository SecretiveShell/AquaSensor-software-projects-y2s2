"""all security related functions."""

from datetime import timedelta
from secrets import token_hex
from argon2 import PasswordHasher

from fastapi.security import APIKeyHeader
from typing import Annotated
from fastapi import Depends, HTTPException
from sqlalchemy import select, update

from aquasensor_backend.ORM import AsyncSessionLocal, Users
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

    return await get_logged_in_user(token)

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

async def create_user_account(username: str, email: str, password: str):
    """create a new user account"""
    
    new_user = Users(
        username=username,
        email=email,
        password=hash_password(password),
    )

    try:
        async with AsyncSessionLocal() as session:
            session.add(new_user)
            await session.commit()

    except Exception:
        return False
    
    return True

async def validate_username_password(username: str, password: str) -> tuple[bool, str, str]:
    """validate a username and password"""

    async with AsyncSessionLocal() as session:
        stmt = select(Users).where(Users.username == username)
        result = await session.execute(stmt)
        user = result.scalars().first()

    if user is None:
        return False, "Invalid username or password.", None

    # use compare_digest to prevent timing attacks
    p = PasswordHasher()
    try:
        p.verify(user.password, password)
    except Exception:
        return False, "Invalid username or password.", None
    
    if p.check_needs_rehash(user.password):
        hash = p.hash(password)
        up = (
            update(Users).where(Users.username == username).values(password=hash)
        )
        await session.execute(up)

    return True, "", user.email
