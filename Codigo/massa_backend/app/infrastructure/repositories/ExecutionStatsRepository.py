from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import extract
from app.api.schemas.ExecutionStatsSchema import ExecutionStatsInput, ExecutionStatsListOutput, ExecutionStatsOutput
from app.domain.models.ExecutionModel import Execution
from app.domain.models.ExecutionStatsModel import ExecutionStats
from app.domain.models.mappers.ExecutionStatsMapper import convert_stats_to_execution_stats_list_output, convert_stats_to_execution_stats_output


class ExecutionStatsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ExecutionStatsInput) -> ExecutionStatsOutput:
        exec_stats = ExecutionStats(**data.model_dump(exclude_none=True))
        try:
            self.session.add(exec_stats)
            await self.session.commit()
            await self.session.refresh(exec_stats)
            return convert_stats_to_execution_stats_output(exec_stats)
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Error creating execution stats: {str(e)}")

    async def update(self, data: ExecutionStatsInput, execution_id: int) -> ExecutionStatsOutput | None:
        async with self.session.begin():
            result = await self.session.execute(select(ExecutionStats).filter_by(execution_id=execution_id))
            exec_stats = result.scalars().first()
            if exec_stats:
                exec_stats.molecule_count = data.molecule_count
                exec_stats.biological_activity_count = data.biological_activity_count
                try:
                    await self.session.commit()
                    return convert_stats_to_execution_stats_output(exec_stats)
                except Exception as e:
                    await self.session.rollback()
                    raise RuntimeError(f"Error updating execution stats: {str(e)}")
            return None

    async def get_stats_by_execution_id(self, execution_id: int) -> ExecutionStatsOutput | None:
        result = await self.session.execute(
            select(ExecutionStats).where(ExecutionStats.execution_id == execution_id)
        )
        exec_stats = result.scalars().first()

        if exec_stats:
            return convert_stats_to_execution_stats_output(exec_stats)

        return None

    async def get_monthly_stats_with_execution_info(self, month: int) -> list[ExecutionStatsListOutput]:
        if not 1 <= month <= 12:
            raise ValueError("Invalid month. Must be between 1 and 12")

        stmt = (
            select(ExecutionStats, Execution.start_time, Execution.end_time)
            .join(Execution, ExecutionStats.execution_id == Execution.id)
            .where(extract('month', Execution.start_time) == month)
        )

        try:
            result = await self.session.execute(stmt)
            stats_list = result.all()
            response = [
                convert_stats_to_execution_stats_list_output(stats, start_time, end_time)
                for stats, start_time, end_time in stats_list
            ]
            return response
        except Exception as e:
            await self.session.rollback()
            raise RuntimeError(f"Error retrieving execution stats list: {str(e)}")