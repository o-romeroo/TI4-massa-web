from sqlalchemy import Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.models.BaseModel import Base
from app.domain.models.ExecutionModel import Execution

class ExecutionStats(Base):
    __tablename__ = "execution_stats"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[int] = mapped_column(ForeignKey("executions.id"))
    execution: Mapped["Execution"] = relationship(back_populates="stats", single_parent=True)
    molecule_count: Mapped[int] = mapped_column(Integer, default=None)
    biological_activity_count: Mapped[int] = mapped_column(Integer, default=None)

    __table_args__ = (
        UniqueConstraint("execution_id"),
    )