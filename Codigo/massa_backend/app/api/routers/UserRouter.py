from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.UserSchema import UserAdressOutput, UserOutput, CreateUserInput, AuthUserOutput, UserLoginInput
from app.domain.services.UserService import UserService
from app.infrastructure.Database import get_async_db_connection


UserRouter = APIRouter(
    prefix="/users",
    tags=["user"]
)

@UserRouter.post("/register", status_code=201, response_model=AuthUserOutput)
async def create_user(data: CreateUserInput, session: AsyncSession = Depends(get_async_db_connection)):
    _service = UserService(session)
    return await _service.create_user(data)

@UserRouter.post("/login", status_code=200, response_model=AuthUserOutput)
async def login_user(data: UserLoginInput, session: AsyncSession = Depends(get_async_db_connection)):
    _service = UserService(session)
    return await _service.login_user(data)

@UserRouter.get("/{user_id}", status_code=200, response_model=UserOutput)
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_db_connection)) -> UserOutput:
    _service = UserService(session)
    return await _service.get_user(user_id)

@UserRouter.get("/all/addresses", status_code=200, response_model=list[UserAdressOutput])
async def get_all_user_adress(session: AsyncSession = Depends(get_async_db_connection)):
    _service = UserService(session)
    return await _service.get_all_user_adress()


