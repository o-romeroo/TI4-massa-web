from sqlalchemy import Integer, ForeignKey, LargeBinary, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.domain.models.BaseModel import Base
from app.domain.models.ExecutionModel import Execution

class ResultModel(Base):
    __tablename__ = 'results'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_id: Mapped[int] = mapped_column(ForeignKey("executions.id"))

    biological_hca_euclidian_distances: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    physicochemical_hca_euclidian_distances: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    structural_hca_euclidian_distances: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    biological_clustering_dataset_dist: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    structural_clustering_dataset_dist: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    physicochemical_clustering_dataset_dist: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    general_clustering_dataset_dist: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    biological_activity_hca: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    physicochemical_properties_hca: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)
    atom_pairs_fingerprint_hca: Mapped[bytes] = mapped_column(LargeBinary, nullable=True)

    execution: Mapped["Execution"] = relationship(back_populates="result_model", single_parent=True)

    __table_args__ = (
        UniqueConstraint("execution_id"),
    )
