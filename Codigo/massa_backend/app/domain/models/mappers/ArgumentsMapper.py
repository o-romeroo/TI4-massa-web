from app.api.schemas.ArgumentsSchema import ArgumentsInput, ArgumentsOutput
from app.domain.models.ArgumentsModel import Arguments

def convert_arguments_to_output(arguments: Arguments) -> ArgumentsOutput:
    return ArgumentsOutput(
        id=arguments.id,
        execution_id=arguments.execution_id,
        number_of_PCs=arguments.number_of_PCs,
        svd_solver_for_PCA=arguments.svd_solver_for_PCA,
        dendrograms_x_axis_font_size=arguments.dendrograms_x_axis_font_size,
        bar_plots_x_axis_font_size=arguments.bar_plots_x_axis_font_size,
        linkage_method=arguments.linkage_method,
        plot_dendrogram=arguments.plot_dendrogram,
        biological_activities=arguments.biological_activities,
        percentage_of_molecules=arguments.percentage_of_molecules,  # Certifique-se de que essa propriedade existe no modelo.
    )

def convert_output_to_arguments(arguments_output: ArgumentsOutput) -> Arguments:
    return Arguments(
        id=arguments_output.id,
        execution_id=arguments_output.execution_id,
        percentage_of_molecules=arguments_output.percentage_of_molecules,
        number_of_PCs=arguments_output.number_of_PCs,
        svd_solver_for_PCA=arguments_output.svd_solver_for_PCA,
        dendrograms_x_axis_font_size=arguments_output.dendrograms_x_axis_font_size,
        bar_plots_x_axis_font_size=arguments_output.bar_plots_x_axis_font_size,
        linkage_method=arguments_output.linkage_method,
        plot_dendrogram=arguments_output.plot_dendrogram,
        biological_activities=arguments_output.biological_activities,
    )

def convert_input_to_arguments(arguments_input: ArgumentsInput) -> Arguments:
    return Arguments(
        execution_id=arguments_input.execution_id,
        percentage_of_molecules=arguments_input.percentage_of_molecules,
        number_of_PCs=arguments_input.number_of_PCs,
        svd_solver_for_PCA=arguments_input.svd_solver_for_PCA.value,
        dendrograms_x_axis_font_size=arguments_input.dendrograms_x_axis_font_size,
        bar_plots_x_axis_font_size=arguments_input.bar_plots_x_axis_font_size,
        linkage_method=arguments_input.linkage_method.value,
        plot_dendrogram=arguments_input.plot_dendrogram,
        biological_activities=arguments_input.biological_activities,
    )
