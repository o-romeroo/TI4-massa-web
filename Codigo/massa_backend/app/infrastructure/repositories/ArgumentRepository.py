from typing import Optional, Type
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.domain.models.ArgumentsModel import Arguments
from app.api.schemas.ArgumentsSchema import ArgumentsInput, ArgumentsOutput
from app.domain.models.ExecutionModel import Execution, ExecutionStatus
from app.domain.models.mappers.ArgumentsMapper import convert_arguments_to_output


class ArgumentsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ArgumentsInput) -> ArgumentsOutput:
        try:
            arguments = Arguments(**data.arguments.model_dump(exclude_none=True))
            self.session.add(arguments)
            await self.session.commit()
            await self.session.refresh(arguments)
            return convert_arguments_to_output(arguments)
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_arguments(self, arguments_id: int) -> Optional[ArgumentsOutput]:
        result = await self.session.execute(
            select(Arguments).where(Arguments.id == arguments_id)
        )
        arguments = result.scalars().first()
        if arguments:
            return convert_arguments_to_output(arguments)
        return None

    async def get_execution_by_id(self, execution_id: int) -> Optional[Execution]:
        result = await self.session.execute(
            select(Execution).where(Execution.id == execution_id)
        )
        return result.scalars().first()

    async def update_status(self, execution_id: int, status: ExecutionStatus):
        result = await self.session.execute(
            select(Execution).where(Execution.id == execution_id)
        )
        execution = result.scalars().first()

        if not execution:
            raise RuntimeError("Execution not found")

        execution.status = status
        try:
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise RuntimeError("Error updating execution status")

    async def delete(self, arguments: Arguments) -> bool:
        try:
            await self.session.delete(arguments)
            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            return False
