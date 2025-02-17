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
from aquasensor_backend.security import hash_password
from aquasensor_backend.ORM import Users, AsyncSessionLocal

router = APIRouter()


@router.post("/login")
async def login(login: Login) -> LoginResponse:
    """log in to your account and return a token"""
    pass


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
async def me() -> UserModel:
    """get information about the currently logged in user"""
    pass
