from typing import List, Optional

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.schemas.ArgumentsSchema import ArgumentsInput
from app.api.schemas.ExecutionSchema import ExecutionInput, ExecutionOutput
from app.api.schemas.ExecutionStatsSchema import ExecutionStatsInput
from app.domain.models.ArgumentsModel import Arguments
from app.domain.models.ExecutionModel import Execution
from app.domain.models.ExecutionStatsModel import ExecutionStats
from app.domain.models.mappers.ExecutionMapper import convert_execution_to_output


class ExecutionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ExecutionInput) -> ExecutionOutput:
        try:
            execution = Execution(
                user_id=data.user_id,
                start_time=data.start_time,
                end_time=data.end_time,
                status=data.status,
            )
            self.session.add(execution)
            await self.session.commit()
            await self.session.refresh(execution)

            # Criação de argumentos (usando execution_id gerado)
            if hasattr(data, 'arguments') and data.arguments:
                arguments_data = (
                    data.arguments.model_dump(exclude_none=True)
                    if isinstance(data.arguments, ArgumentsInput)
                    else data.arguments
                )
                arguments = Arguments(**arguments_data)
                arguments.execution_id = execution.id
                self.session.add(arguments)
                execution.arguments = arguments

            # Criação de stats (usando execution_id gerado)
            if hasattr(data, 'stats') and data.stats:
                stats_data = (
                    data.stats.model_dump(exclude_none=True)
                    if isinstance(data.stats, ExecutionStatsInput)
                    else data.stats
                )
                stats = ExecutionStats(**stats_data)
                stats.execution_id = execution.id
                self.session.add(stats)
                execution.stats = stats

            await self.session.commit()
            await self.session.refresh(execution)

            return convert_execution_to_output(execution)

        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Erro ao criar execução: {str(e)}")

    async def get_all(self) -> List[ExecutionOutput]:
        result = await self.session.execute(select(Execution))
        executions = result.scalars().all()

        response: List[ExecutionOutput] = [
            convert_execution_to_output(execution)
            for execution in executions
            if isinstance(execution, Execution)
        ]

        return response

    async def get_execution(self, _id: int) -> Optional[ExecutionOutput]:
        result = await self.session.execute(
            select(Execution).where(Execution.id == _id)
        )
        execution = result.scalars().first()

        if execution:
            return convert_execution_to_output(execution)

        return None

    async def update(self, execution_id: int, data: ExecutionInput) -> Optional[ExecutionOutput]:
        result = await self.session.execute(
            select(Execution).where(Execution.id == execution_id)
        )
        exec_updt = result.scalars().first()

        if not exec_updt:
            return None

        exec_updt.status = data.status
        exec_updt.end_time = data.end_time

        try:
            await self.session.commit()
            await self.session.refresh(exec_updt)
            return convert_execution_to_output(exec_updt)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Erro ao atualizar execução: {str(e)}")

    async def delete(self, execution: Execution) -> bool:
        try:
            await self.session.delete(execution)
            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            return False
