from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.UserSchema import CreateUserInput, UserAdressOutput, UserOutput, AuthUserOutput, UserLoginInput
from app.core.Security import JWTAuth, PasswordHandler
from app.domain.models.mappers.UserMapper import convert_output_to_user, \
    convert_create_user_input_to_user
from app.infrastructure.repositories.UserRepository import UserRepository


class UserService:

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.auth_handler = JWTAuth()
        self.password_handler = PasswordHandler()

    async def create_user(self, data: CreateUserInput) -> AuthUserOutput:
        hashed_pw = self.password_handler.get_password_hash(data.password)
        data.password = hashed_pw

        try:
            # Chama o repositório para criar o usuário
            created_user = await self.repository.create(data)
            # Criação do token de acesso para o usuário
            token = self.auth_handler.create_access_token(created_user.id)
            # Retorna o token e o ID da sessão do usuário
            return AuthUserOutput(token=token)
        except Exception as e:
            await self.repository.session.rollback()  # Rollback assíncrono
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

    async def login_user(self, data: UserLoginInput) -> AuthUserOutput:
        user = await self.repository.get_user_by_username(data.username)

        if not user or not self.password_handler.verify_password(data.password, user.password_hash):
            raise HTTPException(
                status_code=401,
                detail=f"Invalid credentials for {str(data.username)}",
                headers={"WWW-Authenticate": "Bearer"}
        )

        token = self.auth_handler.create_access_token(user.id)

        return AuthUserOutput(token=token)

    async def get_user(self, user_id: int) -> UserOutput:
        user = await self.repository.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def get_all_user_adress(self) -> list[UserAdressOutput]:
        return await self.repository.get_all_user_adress()

    async def update_user(self, data: CreateUserInput, user_id: int) -> UserOutput:
        hashed_pw = self.password_handler.get_password_hash(data.password)
        data.password = hashed_pw

        user = convert_create_user_input_to_user(data)
        updated_user = await self.repository.update(user, user_id)

        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found")
        return updated_user

    async def delete_user(self, user_id: int) -> bool:
        # Verifica se o usuário existe antes de tentar deletar
        output = await self.repository.get_user(user_id)
        if not output:
            raise HTTPException(status_code=404, detail="User not found")
        
        user = convert_output_to_user(output)

        try:
            return await self.repository.delete(user)
        except Exception as e:
            await self.repository.session.rollback()  # Rollback assíncrono
            raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
