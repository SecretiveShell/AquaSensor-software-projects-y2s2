from typing import Annotated

from sqlalchemy import select, update
from aquasensor_backend.ORM import AsyncSessionLocal, Users
from aquasensor_backend.cache import cache
from fastapi import APIRouter, Depends
from aquasensor_backend.models.auth import (
    Login,
    LoginResponse,
    LogoutResponse,
    Register,
    RegisterResponse,
    UserModel,
)
from aquasensor_backend.security import (
    create_login_session,
    create_user_account,
    hash_password,
    get_logged_in_user_depends,
    api_key_header,
    validate_username_password,
)

from argon2 import PasswordHasher

router = APIRouter()


@router.post("/login")
async def login(login: Login) -> LoginResponse:
    """log in to your account and return a token"""

    valid, message, email = await validate_username_password(login.username, login.password)

    if valid:
        token = await create_login_session(login.username, email)
        return LoginResponse(success=True, token=token)
    
    return LoginResponse(success=False, message=message)


@router.post("/register")
async def register(register: Register) -> RegisterResponse:
    """register a new user account"""

    success = await create_user_account(register.username, register.email, register.password)
    
    if not success:
        return RegisterResponse(success=False, failure_reason="Username already taken.")
    
    token = await create_login_session(register.username, register.email)

    return RegisterResponse(success=True, token=token)


@router.get("/logout")
async def logout(token: Annotated[str, Depends(api_key_header)]) -> LogoutResponse:
    """log out and invalidate the token"""

    await cache.delete(token)

    return {"success": True}


@router.get("/me")
async def me(logged_in_user: get_logged_in_user_depends) -> UserModel:
    """get information about the currently logged in user"""

    return logged_in_user
