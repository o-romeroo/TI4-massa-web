from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.schemas.ExecutionSchema import ExecutionInput, ExecutionOutput
from app.domain.models.ExecutionModel import Execution, ExecutionStatus
from app.domain.models.mappers.ExecutionMapper import convert_execution_to_output, convert_output_to_execution
from app.infrastructure.repositories.ExecutionRepository import ExecutionRepository


class ExecutionService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = ExecutionRepository(session)

    async def create_execution(self, data: ExecutionInput) -> ExecutionOutput:
        try:
            return await self.repository.create(data)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Error creating execution: {str(e)}")

    async def get_execution(self, execution_id: int) -> Optional[Execution]:
        result = await self.session.execute(
            select(Execution).where(Execution.id == execution_id)
        )
        return result.scalars().first()

    async def update_execution(self, execution_id: int, data: ExecutionInput) -> ExecutionOutput:
        execution = await self.repository.update(execution_id, data)

        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        return execution

    async def update_execution_status(self, execution_id: int, status: ExecutionStatus) -> Execution:
        result = await self.session.execute(
            select(Execution).where(Execution.id == execution_id)
        )
        execution = result.scalars().first()

        if not execution:
            raise RuntimeError("Execution not found")

        execution.status = status

        try:
            await self.session.commit()
            await self.session.refresh(execution)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Error updating execution status: {str(e)}")

        return execution

    async def delete_execution(self, execution_id: int):
        output = await self.repository.get_execution(execution_id)

        if not output:
            raise HTTPException(status_code=404, detail="Execution not found")

        execution = convert_output_to_execution(output)

        try:
            await self.repository.delete(execution)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Error deleting execution: {str(e)}")
