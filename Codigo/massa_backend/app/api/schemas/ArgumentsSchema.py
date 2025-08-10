from pydantic import BaseModel, Field

from app.domain.constants import DefaultArgumentValues
from app.domain.models.ArgumentsModel import SVDSolver, LinkageMethod


class ArgumentsInput(BaseModel):
    execution_id: int  
    percentage_of_molecules: float = Field(default=DefaultArgumentValues.DEFAULT_PERCENTAGE_OF_MOLECULES)
    number_of_PCs: float = Field(default=DefaultArgumentValues.DEFAULT_NUMBER_OF_PCS)
    svd_solver_for_PCA: SVDSolver = Field(default=SVDSolver.FULL)
    dendrograms_x_axis_font_size: int = Field(
        default=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_DENDROGRAMS
    )
    bar_plots_x_axis_font_size: int = Field(
        default=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_BAR_PLOTS
    )
    linkage_method: LinkageMethod = Field(default=LinkageMethod.COMPLETE)
    plot_dendrogram: bool = Field(default=True)
    biological_activities: list[str] 

class ArgumentsOutput(BaseModel):
    id: int
    execution_id: int
    percentage_of_molecules: float
    number_of_PCs: float
    svd_solver_for_PCA: SVDSolver
    dendrograms_x_axis_font_size: int
    bar_plots_x_axis_font_size: int
    linkage_method: LinkageMethod
    plot_dendrogram: bool
    biological_activities: list[str]