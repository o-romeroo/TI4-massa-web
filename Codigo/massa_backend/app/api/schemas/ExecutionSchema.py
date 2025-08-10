from datetime import datetime
from pydantic import BaseModel, Field

from app.api.schemas.ArgumentsSchema import ArgumentsInput, ArgumentsOutput
from app.api.schemas.ExecutionStatsSchema import ExecutionStatsInput, ExecutionStatsOutput
from app.domain.models.ExecutionModel import ExecutionStatus
from typing import Optional

class ExecutionInput(BaseModel):
    user_id: int
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = Field(default=None)  
    status: ExecutionStatus = Field(default=ExecutionStatus.IDLE)
    stats: Optional[ExecutionStatsInput] = Field(default=None)  



class ExecutionOutput(BaseModel):
    id: int
    user_id: int
    start_time: datetime 
    end_time: Optional[datetime] = Field(default=None) 
    status: ExecutionStatus
    stats: Optional[ExecutionStatsOutput] = Field(default=None)  
