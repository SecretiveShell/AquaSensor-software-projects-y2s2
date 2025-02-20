from pydantic import BaseModel, EmailStr, Field


class Login(BaseModel):
    """Login Data"""

    username: str = Field(..., description="Username")
    password: str = Field(..., description="Password")


class LoginResponse(BaseModel):
    """Login Response"""

    success: bool = Field(..., description="Success")
    token: str | None = Field(None, description="Token")


class Register(BaseModel):
    """Register Data"""

    username: str = Field(..., description="Username", min_length=3, max_length=20)
    email: EmailStr = Field(..., description="Email")
    password: str = Field(..., description="Password", min_length=16, max_length=72)


class RegisterResponse(BaseModel):
    """Register Response"""

    success: bool = Field(..., description="Success")
    token: str | None = Field(None, description="Session Token")
    failure_reason: str | None = Field(None, description="Failure Reason")


class UserModel(BaseModel):
    """User Model"""

    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email")


class LogoutResponse(BaseModel):
    success: bool = Field(True, description="Success")
