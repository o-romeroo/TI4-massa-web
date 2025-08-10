from datetime import datetime
from app.api.schemas.ExecutionStatsSchema import ExecutionStatsListOutput, ExecutionStatsOutput
from app.domain.models.ExecutionStatsModel import ExecutionStats


def convert_stats_to_execution_stats_output(stats: ExecutionStats) -> ExecutionStatsOutput:
    return ExecutionStatsOutput(
        id=stats.id,
        execution_id=stats.execution_id,
        molecule_count=stats.molecule_count,
        biological_activity_count=stats.biological_activity_count
    )

def convert_output_to_execution_stats(stats_output: ExecutionStatsOutput) -> ExecutionStats:
    return ExecutionStats(
        id=stats_output.id,
        execution_id=stats_output.execution_id,
        molecule_count=stats_output.molecule_count,
        biological_activity_count=stats_output.biological_activity_count
    )

def convert_stats_to_execution_stats_list_output(stats: ExecutionStats, start_time: datetime, end_time: datetime) -> ExecutionStatsListOutput:
    return ExecutionStatsListOutput(
        execution_id=stats.execution_id,
        molecule_count=stats.molecule_count,
        biological_activity_count=stats.biological_activity_count,
        start_time=start_time,
        end_time=end_time
    )