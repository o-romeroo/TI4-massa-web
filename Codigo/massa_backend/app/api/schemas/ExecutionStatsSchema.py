from datetime import datetime
from pydantic import BaseModel, Field


class ExecutionStatsInput(BaseModel):
    execution_id: int
    molecule_count: int = Field(ge=0, default=None)
    biological_activity_count: int = Field(ge=0, default=None)

class ExecutionStatsOutput(BaseModel):
    id: int
    execution_id: int
    molecule_count: int
    biological_activity_count: int

class ExecutionStatsListOutput(BaseModel):
    execution_id: int
    molecule_count: int
    biological_activity_count: int
    start_time: datetime
    end_time: datetime

class BiologicalAcitivitiesPerDay(BaseModel):
    sunday: int = 0
    monday: int = 0
    tuesday: int = 0
    wednesday: int = 0
    thursday: int = 0
    friday: int = 0
    saturday: int = 0

class MonthlyExecutionStatsOutput(BaseModel):
    molecule_count_avg: float
    biological_activity_total: int
    biological_activities_per_day: BiologicalAcitivitiesPerDay