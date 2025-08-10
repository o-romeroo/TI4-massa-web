from app.api.schemas.ExecutionSchema import ExecutionOutput, ExecutionInput
from app.domain.models.ArgumentsModel import Arguments
from app.domain.models.ExecutionModel import Execution
from app.domain.models.ExecutionStatsModel import ExecutionStats
from app.domain.models.mappers.ArgumentsMapper import convert_arguments_to_output, convert_output_to_arguments
from app.domain.models.mappers.ExecutionStatsMapper import convert_stats_to_execution_stats_output, \
    convert_output_to_execution_stats


def convert_execution_to_output(execution: Execution) -> ExecutionOutput:
    return ExecutionOutput(
        id=execution.id,
        user_id=execution.user_id,
        arguments=convert_arguments_to_output(execution.arguments) if execution.arguments else None,
        start_time=execution.start_time,
        end_time=execution.end_time,
        status=execution.status,
        stats=convert_stats_to_execution_stats_output(execution.stats) if execution.stats else None,
    )


def convert_input_to_execution(exec_input: ExecutionInput, arguments: Arguments, stats: ExecutionStats) -> Execution:
    return Execution(
        user_id=exec_input.user_id,
        arguments=arguments,
        start_time=exec_input.start_time,
        end_time=exec_input.end_time,
        status=exec_input.status,
        stats=stats
    )

def convert_output_to_execution(exec_output: ExecutionOutput) -> Execution:
    return Execution(
        id=exec_output.id,
        user_id=exec_output.user_id,
        arguments=convert_output_to_arguments(exec_output.arguments),
        start_time=exec_output.start_time,
        end_time=exec_output.end_time,
        status=exec_output.status,
        stats=convert_output_to_execution_stats(exec_output.stats)
    )