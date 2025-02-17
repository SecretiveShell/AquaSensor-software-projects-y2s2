from datetime import timedelta

from sqlalchemy import select
from aquasensor_backend.ORM import AsyncSessionLocal, Users
from aquasensor_backend.cache import cache
from fastapi import APIRouter
from aquasensor_backend.models.auth import (
    Login,
    LoginResponse,
    Register,
    RegisterResponse,
    UserModel,
)
from aquasensor_backend.security import hash_password, get_logged_in_user_depends
from aquasensor_backend.ORM import Users, AsyncSessionLocal
from secrets import compare_digest, token_hex

router = APIRouter()


@router.post("/login")
async def login(login: Login) -> LoginResponse:
    """log in to your account and return a token"""
    async with AsyncSessionLocal() as session:

        stmt = select(Users).where(Users.username == login.username)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if user is None:
            return LoginResponse(success=False, failure_reason="Invalid username or password.")
        
        # use compare_digest to prevent timing attacks
        if not compare_digest(user.password, hash_password(login.password)):
            return LoginResponse(success=False, failure_reason="Invalid username or password.")
        
        user = UserModel(username=user.username, email=user.email)
        token = token_hex(128)

        await cache.set(token, user, ttl=timedelta(days=1).total_seconds())

        return LoginResponse(success=True, token=token)

@router.post("/register")
async def register(register: Register) -> RegisterResponse:
    """register a new user account"""
    
    new_user = Users(
        username = register.username,
        email = register.email,
        password = hash_password(register.password)
    )

    async with AsyncSessionLocal() as session:
        session.add(new_user)
        await session.commit()

    return RegisterResponse(success=True)


@router.get("/logout")
async def logout():
    """log out and invalidate the token"""
    pass


@router.get("/me")
async def me(logged_in_user: get_logged_in_user_depends) -> UserModel:
    """get information about the currently logged in user"""
    
    return logged_in_user
