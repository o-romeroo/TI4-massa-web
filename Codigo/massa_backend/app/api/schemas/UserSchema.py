from pydantic import BaseModel, Field


class UserOutput(BaseModel):
    id: int
    username: str
    email: str
    country: str
    city: str
    is_active: bool

class UserAdressOutput(BaseModel):
    country: str
    city: str

class CreateUserInput(BaseModel):
    username: str = Field(min_length=6, max_length=30)
    email: str
    password: str = Field(min_length=8, max_length=64)
    country: str = Field(min_length=2, max_length=30)
    city: str = Field(min_length=3, max_length=100)

class AuthUserOutput(BaseModel):
    token: str

class UserLoginInput(BaseModel):
    username: str
    password: str

class UserLoginOutput(BaseModel):
    id: int
    username: str
    email: str
    password_hash: str