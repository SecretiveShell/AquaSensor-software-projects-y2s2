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
    hash_password,
    get_logged_in_user_depends,
    api_key_header,
)

from argon2 import PasswordHasher

router = APIRouter()


@router.post("/login")
async def login(login: Login) -> LoginResponse:
    """log in to your account and return a token"""
    async with AsyncSessionLocal() as session:
        stmt = select(Users).where(Users.username == login.username)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user is None:
            return LoginResponse(
                success=False, failure_reason="Invalid username or password."
            )

        # use compare_digest to prevent timing attacks
        p = PasswordHasher()
        try:
            p.verify(user.password, login.password)
        except Exception:
            return LoginResponse(
                success=False, failure_reason="Invalid username or password."
            )
        if p.check_needs_rehash(user.password):
            h = p.hash(login.password)
            up = (
                update(Users).where(Users.username == login.username).values(password=h)
            )
            await session.execute(up)

        token = await create_login_session(user.username, user.email)

        return LoginResponse(success=True, token=token)


@router.post("/register")
async def register(register: Register) -> RegisterResponse:
    """register a new user account"""

    new_user = Users(
        username=register.username,
        email=register.email,
        password=hash_password(register.password),
    )

    try:
        async with AsyncSessionLocal() as session:
            session.add(new_user)
            await session.commit()

    except Exception:
        return RegisterResponse(
            success=False, failure_reason="This account already exists."
        )

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
