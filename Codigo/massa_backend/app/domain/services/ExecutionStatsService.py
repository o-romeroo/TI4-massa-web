from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.ExecutionStatsSchema import ExecutionStatsInput, ExecutionStatsListOutput, ExecutionStatsOutput, \
    MonthlyExecutionStatsOutput, BiologicalAcitivitiesPerDay
from app.infrastructure.repositories.ExecutionStatsRepository import ExecutionStatsRepository


class ExecutionStatsService:

    def __init__(self, session: AsyncSession):
        self.repository = ExecutionStatsRepository(session)

    async def create_stats(self, data: ExecutionStatsInput):
        try:
            return await self.repository.create(data)
        except Exception as e:
            await self.repository.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating stats: {str(e)}")

    async def update_stats(self, execution_id: int, data: ExecutionStatsInput) -> ExecutionStatsOutput:
        stats = await self.repository.update(data, execution_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Stats not found")
        return stats

    async def get_stats_by_execution(self, execution_id: int) -> ExecutionStatsOutput:
        stats = await self.repository.get_stats_by_execution_id(execution_id)

        if not stats:
            raise HTTPException(status_code=404, detail="Stats not found")

        return stats

    async def get_monthly_execution_stats(self) -> MonthlyExecutionStatsOutput:
        current_month = datetime.now(timezone.utc).month

        stats = await self.repository.get_monthly_stats_with_execution_info(current_month)

        if not stats:
            return MonthlyExecutionStatsOutput(
                molecule_count_avg=0,
                biological_activity_total=0,
                biological_activities_per_day=BiologicalAcitivitiesPerDay()
            )

        molecule_count_avg = sum(stat.molecule_count for stat in stats) / len(stats)

        biological_activity_total = sum(stat.biological_activity_count for stat in stats)

        biological_activities_per_day = BiologicalAcitivitiesPerDay()

        for stat in stats:
            day_of_week = stat.start_time.weekday()

            if day_of_week == 0:
                biological_activities_per_day.monday += stat.biological_activity_count
            elif day_of_week == 1:
                biological_activities_per_day.tuesday += stat.biological_activity_count
            elif day_of_week == 2:
                biological_activities_per_day.wednesday += stat.biological_activity_count
            elif day_of_week == 3:
                biological_activities_per_day.thursday += stat.biological_activity_count
            elif day_of_week == 4:
                biological_activities_per_day.friday += stat.biological_activity_count
            elif day_of_week == 5:
                biological_activities_per_day.saturday += stat.biological_activity_count
            elif day_of_week == 6:
                biological_activities_per_day.sunday += stat.biological_activity_count

        return MonthlyExecutionStatsOutput(
            molecule_count_avg=round(molecule_count_avg, 2),
            biological_activity_total=biological_activity_total,
            biological_activities_per_day=biological_activities_per_day,
        )