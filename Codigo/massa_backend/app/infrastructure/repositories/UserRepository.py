from typing import Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select  

from app.domain.models.UserModel import User
from app.api.schemas.UserSchema import UserAdressOutput, UserOutput, UserLoginOutput
from app.api.schemas.UserSchema import CreateUserInput
from app.domain.models.mappers.UserMapper import convert_user_to_output, convert_user_to_user_login_output, \
    convert_create_user_input_to_user
from sqlalchemy import delete

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CreateUserInput) -> UserOutput:
        user = convert_create_user_input_to_user(data)

        self.session.add(user)
        try:
            await self.session.commit()  
            await self.session.refresh(user)  
            return convert_user_to_output(user)
        except SQLAlchemyError as e:
            await self.session.rollback()  
            raise Exception(f"Error creating user: {str(e)}")

    async def get_user(self, user_id: int) -> Optional[UserOutput]:
        result = await self.session.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()

        if user:
            return convert_user_to_output(user)

        return None
    
    async def get_all_user_adress(self) -> list[UserAdressOutput]:
        try:
            result = await self.session.execute(
                select(User.country, User.city).distinct()
            )
            distinct_addresses = result.all()

            return [UserAdressOutput(country=country, city=city) for country, city in distinct_addresses]
        except SQLAlchemyError as e:
            raise Exception(f"Error fetching user addresses: {str(e)}")

    async def get_user_by_username(self, username: str) -> UserLoginOutput | None:
        async with self.session.begin():
            result = await self.session.execute(select(User).filter_by(username=username))
            user = result.scalars().first()

            if user:
                return convert_user_to_user_login_output(user)
            return None

    async def update(self, user: User, user_id: int) -> UserOutput | None:
        async with self.session.begin():
            result = await self.session.execute(select(User).filter_by(id=user_id))  
            user_updt = result.scalars().first()  
            if user_updt:
                user_updt.country = user.country
                user_updt.city = user.city
                try:
                    await self.session.commit()  
                    return convert_user_to_output(user_updt)
                except SQLAlchemyError as e:
                    await self.session.rollback()  
                    raise Exception(f"Error updating user: {str(e)}")
            return None

    async def delete(self, user: User) -> bool:
        try:
            await self.session.execute(delete(User).where(User.id == user.id))  
            await self.session.commit()  
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()  
            raise Exception(f"Error deleting user: {str(e)}")
