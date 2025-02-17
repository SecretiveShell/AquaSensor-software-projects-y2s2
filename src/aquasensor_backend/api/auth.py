from aquasensor_backend.ORM import AsyncSessionLocal, Users
from aquasensor_backend.cache import cache
from fastapi import APIRouter
from aquasensor_backend.models.auth import Login, LoginResponse, Register, RegisterResponse, UserModel

router = APIRouter()

@router.post("/login")
async def login(login: Login) -> LoginResponse:
    """log in to your account and return a token"""
    pass

@router.post("/register")
async def register(register: Register) -> RegisterResponse:
    """register a new user account"""
    pass

@router.get("/logout")
async def logout():
    """log out and invalidate the token"""
    pass

@router.get("/me")
async def me() -> UserModel:
    """get information about the currently logged in user"""
    pass
