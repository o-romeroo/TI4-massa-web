from sqlalchemy import Float, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as TableEnum

from enum import Enum
from app.domain.models.BaseModel import Base
from app.domain.constants import DefaultArgumentValues
from app.domain.models.ExecutionModel import Execution

class SVDSolver(Enum):
    AUTO = "auto"
    FULL = "full"
    COVARIANCE_EIGH = "covariance_eigh"
    ARPACK = "arpack"
    RANDOMIZED = "randomized"

class LinkageMethod(Enum):
    SINGLE = "single"
    COMPLETE = "complete"
    AVERAGE = "average"
    WEIGHTED = "weighted"
    CENTROID = "centroid"
    MEDIAN = "median"
    WARD = "ward"

class Arguments(Base):
    __tablename__ = "arguments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[int] = mapped_column(ForeignKey("executions.id"))
    execution: Mapped["Execution"] = relationship(back_populates="arguments", single_parent=True)
    percentage_of_molecules: Mapped[float] = (
        mapped_column(Float, default=DefaultArgumentValues.DEFAULT_PERCENTAGE_OF_MOLECULES)
    )
    number_of_PCs: Mapped[float] = mapped_column(Float, default=DefaultArgumentValues.DEFAULT_NUMBER_OF_PCS)
    svd_solver_for_PCA: Mapped[SVDSolver] = mapped_column(TableEnum(SVDSolver), default=SVDSolver.FULL)

    dendrograms_x_axis_font_size: Mapped[int] = (
        mapped_column(Integer, default=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_DENDROGRAMS)

    )

    bar_plots_x_axis_font_size: Mapped[int] = (
        mapped_column(Integer, default=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_BAR_PLOTS)
    )

    linkage_method: Mapped[LinkageMethod] = mapped_column(TableEnum(LinkageMethod), default=LinkageMethod.COMPLETE)

    plot_dendrogram: Mapped[bool] = mapped_column(Boolean, default=True)

    biological_activities: Mapped[list] = mapped_column(JSONB)

    __table_args__ = (
        UniqueConstraint("execution_id"),
    )