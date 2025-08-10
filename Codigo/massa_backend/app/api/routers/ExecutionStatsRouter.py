from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.ExecutionStatsSchema import ExecutionStatsListOutput, MonthlyExecutionStatsOutput

from app.domain.services.ExecutionStatsService import ExecutionStatsService
from app.infrastructure.Database import get_async_db_connection
from app.infrastructure.repositories.ExecutionStatsRepository import ExecutionStatsRepository

ExecutionStatsRouter = APIRouter(
    prefix="/stats",
    tags=["stat"]
)

@ExecutionStatsRouter.get("/monthly", response_model=MonthlyExecutionStatsOutput)
async def get_execution_stats(session: AsyncSession = Depends(get_async_db_connection)):
    service = ExecutionStatsService(session)
    return await service.get_monthly_execution_stats()
