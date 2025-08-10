from app.api.schemas.ResultSchema import ResultOutput, ResultInput, ImagesOutput, DistancePlotsOutput, \
    GraphicsOutput, DistributionPlotsOutput
from app.domain.models.ResultModel import ResultModel
from app.helpers.ImagesUtils import blob_to_base64
from typing import List, Union, Dict


def convert_result_to_output(result: ResultModel) -> ResultOutput:
    return ResultOutput(
        id=result.id,
        execution_id=result.execution_id,
        biological_hca_euclidian_distances=result.biological_hca_euclidian_distances,
        physicochemical_hca_euclidian_distances=result.physicochemical_hca_euclidian_distances,
        structural_hca_euclidian_distances=result.structural_hca_euclidian_distances,
        biological_clustering_dataset_dist=result.biological_clustering_dataset_dist,
        structural_clustering_dataset_dist=result.structural_clustering_dataset_dist,
        physicochemical_clustering_dataset_dist=result.physicochemical_clustering_dataset_dist,
        general_clustering_dataset_dist=result.general_clustering_dataset_dist,
        biological_activity_hca=result.biological_activity_hca,
        physicochemical_properties_hca=result.physicochemical_properties_hca,
        atom_pairs_fingerprint_hca=result.atom_pairs_fingerprint_hca
    )

def convert_result_to_input(result: ResultModel) -> ResultInput:
    return ResultInput(
        id=result.id,
        execution_id=result.execution_id,
        biological_hca_euclidian_distances=result.biological_hca_euclidian_distances,
        physicochemical_hca_euclidian_distances=result.physicochemical_hca_euclidian_distances,
        structural_hca_euclidian_distances=result.structural_hca_euclidian_distances,
        biological_clustering_dataset_dist=result.biological_clustering_dataset_dist,
        structural_clustering_dataset_dist=result.structural_clustering_dataset_dist,
        physicochemical_clustering_dataset_dist=result.physicochemical_clustering_dataset_dist,
        general_clustering_dataset_dist=result.general_clustering_dataset_dist,
        biological_activity_hca=result.biological_activity_hca,
        physicochemical_properties_hca=result.physicochemical_properties_hca,
        atom_pairs_fingerprint_hca=result.atom_pairs_fingerprint_hca
    )

def convert_to_distribution_plots_output(title: str, total: Dict[str, float], training: Dict[str, float], test: Dict[str, float]) -> DistributionPlotsOutput:
    return DistributionPlotsOutput(
        title=title,
        labels= list(total.keys()),
        total= list(total.values()),
        training_set= list(training.values()),
        test_set=list(test.values())
    )

def convert_result_to_images_output(result: ResultModel) -> ImagesOutput:
    return ImagesOutput(
        dendrograms={
            "hca_biological": blob_to_base64(result.biological_activity_hca),
            "hca_physicochemical": blob_to_base64(result.physicochemical_properties_hca),
            "hca_structural": blob_to_base64(result.atom_pairs_fingerprint_hca)
        },
        distance_plots={
            "dist_hca_biological": blob_to_base64(result.biological_hca_euclidian_distances),
            "dist_hca_physicochemical": blob_to_base64(result.physicochemical_hca_euclidian_distances),
            "dist_hca_structural": blob_to_base64(result.structural_hca_euclidian_distances)
        },
        distribution_plots={
            "biological": blob_to_base64(result.biological_clustering_dataset_dist),
            "general": blob_to_base64(result.structural_clustering_dataset_dist),
            "physicochemical": blob_to_base64(result.physicochemical_clustering_dataset_dist),
            "structural": blob_to_base64(result.general_clustering_dataset_dist)
        }
    )


def convert_distances_list_to_output_data(title: str, distances_list: List[Union[float, int]]) -> DistancePlotsOutput:
    return DistancePlotsOutput(
        title=title,
        x=list(range(1, len(distances_list) + 10)),
        y=distances_list
    )