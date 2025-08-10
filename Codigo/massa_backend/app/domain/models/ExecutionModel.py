import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, Integer, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as TableEnum
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.domain.models.BaseModel import Base

if TYPE_CHECKING:
    from app.domain.models.ArgumentsModel import Arguments
    from app.domain.models.ResultModel import ResultModel
    from app.domain.models.ExecutionStatsModel import ExecutionStats

class ExecutionStatus(Enum):
    IDLE = "idle"
    PROCESSING = "processing"
    FINISHED = "finished"
    ERROR = "error"

class Execution(Base):
    __tablename__ = "executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    arguments: Mapped[Optional["Arguments"]] = relationship(back_populates="execution", lazy="joined")
    start_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[ExecutionStatus] = mapped_column(TableEnum(ExecutionStatus), default=ExecutionStatus.IDLE, nullable=False)
    stats: Mapped[Optional["ExecutionStats"]] = relationship(back_populates="execution", lazy="joined")
    result_model: Mapped[Optional["ResultModel"]] = relationship(back_populates="execution")
