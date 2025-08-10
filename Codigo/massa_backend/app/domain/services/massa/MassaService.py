from io import FileIO
import os
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import UploadFile

from app.api.schemas.ResultSchema import ImagesOutput, DistancePlotsOutput, GraphicsOutput
from app.domain.models.mappers.ResultMapper import convert_result_to_images_output, \
    convert_distances_list_to_output_data, convert_to_distribution_plots_output
from app.domain.services.ResultService import ResultService
from app.helpers import FileUtils
from app.domain.models.ArgumentsModel import Arguments
from app.domain.services.massa import (MassaReaderService,
                                       MassaExtractionService,
                                       MassaDescriptorsService,
                                       MassaPreparationService,
                                       MassaClusterService,
                                       MassaSplitService)
from app.domain.constants import DefaultArgumentValues
from app.helpers.ImagesUtils import blob_to_base64


async def executeGraphic(arguments: Arguments, result_id, session: AsyncSession, file: UploadFile) -> GraphicsOutput:
    # Obter o conteúdo do arquivo
    file_path = None

    try:
        file_path = await FileUtils.create_temp_file(file)
    except Exception as e:
        print(f"Erro ao criar o arquivo temporário: {e}")
    try:
        molecules = MassaReaderService.read_molecules(file_path)
        sdf_properties_names = MassaReaderService.get_sdf_property_names(molecules)
        added_hydrogen_molecules = MassaReaderService.hydrogen_add(molecules)

        molecules_names, dataframe = MassaExtractionService.name_extraction(added_hydrogen_molecules)
        biological_activities = MassaExtractionService.the_biological_handler(sdf_properties_names,
                                                                            arguments.biological_activities)
        dataframe = MassaExtractionService.list_activities(dataframe, biological_activities)

        dataframe = MassaDescriptorsService.physicochemical_descriptors(dataframe)
        dataframe = MassaDescriptorsService.atompairs_fingerprint(dataframe)

        bio_matrix, PhCh_matrix, FP_matrix = MassaPreparationService.normalizer_or_matrix(dataframe, biological_activities)

        bio_PCA = MassaPreparationService.pca_maker(bio_matrix, arguments.number_of_PCs, arguments.svd_solver_for_PCA)
        PhCh_PCA = MassaPreparationService.pca_maker(PhCh_matrix, arguments.number_of_PCs, arguments.svd_solver_for_PCA)
        FP_PCA = MassaPreparationService.pca_maker(FP_matrix, arguments.number_of_PCs, arguments.svd_solver_for_PCA)

        leaves_cluster_bio, bioHCA, linkage_bio, CutOff_bio, distances_list_bio = await MassaClusterService.hca_clusters(bio_PCA,
                                                                                                                molecules_names,
                                                                                                                'bio',
                                                                                                                DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                                                                arguments.linkage_method,
                                                                                                                result_id,
                                                                                                                session)
        leaves_cluster_phch, phchHCA, linkage_phch, CutOff_phch, distances_list_phch = await MassaClusterService.hca_clusters(
            PhCh_PCA, molecules_names, 'PhCh', DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, arguments.linkage_method,
            result_id, session)
        leaves_cluster_fp, fpHCA, linkage_fp, CutOff_fp, distances_list_fp = await MassaClusterService.hca_clusters(FP_PCA,
                                                                                                            molecules_names,
                                                                                                            'FP',
                                                                                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                                                            arguments.linkage_method,
                                                                                                            result_id,
                                                                                                            session)

        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, bioHCA,
                                                                    'bio')  # It adds the biological cluster identification to the spreadsheet.
        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, phchHCA,
                                                                    'PhCh')  # It adds the physicochemical cluster identification to the spreadsheet.
        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, fpHCA,
                                                                    'FP')  # It adds the structural cluster identification to the spreadsheet.

        matrix_for_kmodes = MassaPreparationService.organize_for_kmodes(dataframe)
        allHCA = MassaClusterService.kmodes_clusters(matrix_for_kmodes, molecules_names)
        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, allHCA, 'all')

        dataframe, test_molecules = MassaSplitService.split_train_test_sets(dataframe, arguments.percentage_of_molecules,
                                                                            __calc_test_percentage(
                                                                                arguments.percentage_of_molecules))

        bio_total, bio_training, bio_test = await MassaSplitService.freq_clusters(dataframe,
                                                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                            'Cluster_Biological',
                                                                            arguments.bar_plots_x_axis_font_size, result_id,
                                                                            session)
        PhCh_total, PhCh_training, PhCh_test = await MassaSplitService.freq_clusters(dataframe,
                                                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                            'Cluster_Physicochemical',
                                                                            arguments.bar_plots_x_axis_font_size,
                                                                            result_id, session)
        FP_total, FP_training, FP_test = await MassaSplitService.freq_clusters(dataframe,
                                                                        DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                        'Cluster_Structural',
                                                                        arguments.bar_plots_x_axis_font_size, result_id,
                                                                        session)
        all_total, all_training, all_test = await MassaSplitService.freq_clusters(dataframe,
                                                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                            'Cluster_General',
                                                                            arguments.bar_plots_x_axis_font_size, result_id,
                                                                            session)

        bio_ok = __returns_zero(bio_total, bio_test)  # For biological domain.
        PhCh_ok = __returns_zero(PhCh_total, PhCh_test)  # For physicochemical domain.
        FP_ok = __returns_zero(FP_total, FP_test)  # For structural domain.
        ok = [bio_ok, PhCh_ok, FP_ok]
        max_iters = 0

        while (True in ok) and (max_iters < 10):
            ## Split into training, test:
            dataframe, test_molecules = MassaSplitService.split_train_test_sets(dataframe,
                                                                                arguments.percentage_of_molecules,
                                                                                __calc_test_percentage(
                                                                                    arguments.percentage_of_molecules))

            ## Bar plot of frequencies (Calculates the percentages of molecules in each cluster for each dataset and generates a bar graph for each domain):
            bio_total, bio_training, bio_test = await MassaSplitService.freq_clusters(dataframe,
                                                                                DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                                'Cluster_Biological',
                                                                                arguments.bar_plots_x_axis_font_size,
                                                                                result_id, session)  # Biological Bar Plot
            PhCh_total, PhCh_training, PhCh_test = await MassaSplitService.freq_clusters(dataframe,
                                                                                DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                                'Cluster_Physicochemical',
                                                                                arguments.bar_plots_x_axis_font_size,
                                                                                result_id,
                                                                                session)  # Physicochemical Bar Plot
            FP_total, FP_training, FP_test = await MassaSplitService.freq_clusters(dataframe,
                                                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                            'Cluster_Structural',
                                                                            arguments.bar_plots_x_axis_font_size,
                                                                            result_id, session)  # Structural Bar Plot
            all_total, all_training, all_test = await MassaSplitService.freq_clusters(dataframe,
                                                                                DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                                'Cluster_General',
                                                                                arguments.bar_plots_x_axis_font_size,
                                                                                result_id, session)  # General Bar Plot

            ## Verifying percentages:
            bio_ok = __returns_zero(bio_total, bio_test)  # For biological domain.
            PhCh_ok = __returns_zero(PhCh_total, PhCh_test)  # For physicochemical domain.
            FP_ok = __returns_zero(FP_total, FP_test)  # For structural domain.
            ok = [bio_ok, PhCh_ok, FP_ok]
            max_iters += 1

    # Plot HCAs:
        if arguments.plot_dendrogram:
            print('\nGenerating dendrogram images. Please wait...')
            await MassaClusterService.hca_plot(linkage_bio, molecules_names, leaves_cluster_bio, CutOff_bio, 'bio',
                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                            arguments.dendrograms_x_axis_font_size,
                                            test_molecules, result_id, session)
            await MassaClusterService.hca_plot(linkage_phch, molecules_names, leaves_cluster_phch, CutOff_phch, 'PhCh',
                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                            arguments.dendrograms_x_axis_font_size,
                                            test_molecules, result_id, session)
            await MassaClusterService.hca_plot(linkage_fp, molecules_names, leaves_cluster_fp, CutOff_fp, 'FP',
                                            DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                            arguments.dendrograms_x_axis_font_size,
                                            test_molecules, result_id, session)

        result = await ResultService(session).get_result_by_id(result_id)
        

        return GraphicsOutput(
            dendrograms={
                "hca_biological": blob_to_base64(result.biological_activity_hca),
                "hca_physicochemical": blob_to_base64(result.physicochemical_properties_hca),
                "hca_structural": blob_to_base64(result.atom_pairs_fingerprint_hca)
            },
            distance_plot={
                "dist_hca_biological": convert_distances_list_to_output_data("Biological", distances_list_bio),
                "dist_hca_physicochemical": convert_distances_list_to_output_data("Physicochemical", distances_list_phch),
                "dist_hca_structural": convert_distances_list_to_output_data("Structural", distances_list_fp)
            },
            distribution_plots={
                "biological": convert_to_distribution_plots_output("Biological Clustering", bio_total, bio_training, bio_test),
                "general": convert_to_distribution_plots_output("General Clustering", all_total, all_training, all_test),
                "physicochemical": convert_to_distribution_plots_output("Physicochemical Clustering", PhCh_total, PhCh_training, PhCh_test),
                "structural": convert_to_distribution_plots_output("Structural Clustering", FP_total, FP_training, FP_test)
            }
        )
    except Exception as e:
        raise RuntimeError(f"Erro durante a execução da análise gráfica: {e}")


async def execute(arguments: Arguments, result_id, session: AsyncSession, file: UploadFile) -> ImagesOutput:
    # Obter o conteúdo do arquivo
    file_path = None

    try:
        file_path = await FileUtils.create_temp_file(file)
    except Exception as e:
        print(f"Erro ao criar o arquivo temporário: {e}")
    try:
        molecules = MassaReaderService.read_molecules(file_path)
        sdf_properties_names = MassaReaderService.get_sdf_property_names(molecules)
        added_hydrogen_molecules = MassaReaderService.hydrogen_add(molecules)

        molecules_names, dataframe = MassaExtractionService.name_extraction(added_hydrogen_molecules)
        biological_activities = MassaExtractionService.the_biological_handler(sdf_properties_names, arguments.biological_activities)
        dataframe = MassaExtractionService.list_activities(dataframe, biological_activities)

        dataframe = MassaDescriptorsService.physicochemical_descriptors(dataframe)
        dataframe = MassaDescriptorsService.atompairs_fingerprint(dataframe)

        bio_matrix, PhCh_matrix, FP_matrix = MassaPreparationService.normalizer_or_matrix(dataframe, biological_activities)

        bio_PCA = MassaPreparationService.pca_maker(bio_matrix, arguments.number_of_PCs, arguments.svd_solver_for_PCA)
        PhCh_PCA = MassaPreparationService.pca_maker(PhCh_matrix, arguments.number_of_PCs, arguments.svd_solver_for_PCA)
        FP_PCA = MassaPreparationService.pca_maker(FP_matrix, arguments.number_of_PCs, arguments.svd_solver_for_PCA)

        leaves_cluster_bio, bioHCA, linkage_bio, CutOff_bio, distances_list_bio = await MassaClusterService.hca_clusters(bio_PCA, molecules_names, 'bio', DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, arguments.linkage_method, result_id, session)
        leaves_cluster_phch, phchHCA, linkage_phch, CutOff_phch, distances_list_phch = await MassaClusterService.hca_clusters(PhCh_PCA, molecules_names, 'PhCh', DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, arguments.linkage_method, result_id, session)
        leaves_cluster_fp, fpHCA, linkage_fp, CutOff_fp, distances_list_fp = await MassaClusterService.hca_clusters(FP_PCA, molecules_names, 'FP', DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, arguments.linkage_method, result_id, session)

        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, bioHCA, 'bio') # It adds the biological cluster identification to the spreadsheet.
        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, phchHCA, 'PhCh') # It adds the physicochemical cluster identification to the spreadsheet.
        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, fpHCA, 'FP') # It adds the structural cluster identification to the spreadsheet.

        matrix_for_kmodes = MassaPreparationService.organize_for_kmodes(dataframe)
        allHCA = MassaClusterService.kmodes_clusters(matrix_for_kmodes, molecules_names)
        dataframe = MassaPreparationService.organize_df_clusterization(dataframe, allHCA, 'all')

        dataframe, test_molecules = MassaSplitService.split_train_test_sets(dataframe, arguments.percentage_of_molecules, __calc_test_percentage(arguments.percentage_of_molecules))

        bio_total, bio_training, bio_test = await MassaSplitService.freq_clusters(dataframe, DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, 'Cluster_Biological', arguments.bar_plots_x_axis_font_size, result_id, session)
        PhCh_total, PhCh_training, PhCh_test = await MassaSplitService.freq_clusters(dataframe, DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, 'Cluster_Physicochemical', arguments.bar_plots_x_axis_font_size, result_id, session)
        FP_total, FP_training, FP_test = await MassaSplitService.freq_clusters(dataframe,  DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, 'Cluster_Structural', arguments.bar_plots_x_axis_font_size, result_id, session)
        all_total, all_training, all_test = await MassaSplitService.freq_clusters(dataframe, DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, 'Cluster_General', arguments.bar_plots_x_axis_font_size, result_id, session)

        bio_ok = __returns_zero(bio_total, bio_test)  # For biological domain.
        PhCh_ok = __returns_zero(PhCh_total, PhCh_test)  # For physicochemical domain.
        FP_ok = __returns_zero(FP_total, FP_test)  # For structural domain.
        ok = [bio_ok, PhCh_ok, FP_ok]
        max_iters = 0

        while (True in ok) and (max_iters < 10):
            ## Split into training, test:
            dataframe, test_molecules = MassaSplitService.split_train_test_sets(dataframe, arguments.percentage_of_molecules, __calc_test_percentage(arguments.percentage_of_molecules))

            ## Bar plot of frequencies (Calculates the percentages of molecules in each cluster for each dataset and generates a bar graph for each domain):
            bio_total, bio_training, bio_test = await MassaSplitService.freq_clusters(dataframe, DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                        'Cluster_Biological', arguments.bar_plots_x_axis_font_size, 
                                                                        result_id, session)  # Biological Bar Plot
            PhCh_total, PhCh_training, PhCh_test = await MassaSplitService.freq_clusters(dataframe, DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                            'Cluster_Physicochemical',arguments.bar_plots_x_axis_font_size, 
                                                                            result_id, session)  # Physicochemical Bar Plot
            FP_total, FP_training, FP_test = await MassaSplitService.freq_clusters(dataframe,DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                    'Cluster_Structural',
                                                                    arguments.bar_plots_x_axis_font_size, 
                                                                    result_id, session)  # Structural Bar Plot
            all_total, all_training, all_test = await MassaSplitService.freq_clusters(dataframe, DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE,
                                                                        'Cluster_General',
                                                                        arguments.bar_plots_x_axis_font_size, 
                                                                        result_id, session)  # General Bar Plot

            ## Verifying percentages:
            bio_ok = __returns_zero(bio_total, bio_test)  # For biological domain.
            PhCh_ok = __returns_zero(PhCh_total, PhCh_test)  # For physicochemical domain.
            FP_ok = __returns_zero(FP_total, FP_test)  # For structural domain.
            ok = [bio_ok, PhCh_ok, FP_ok]
            max_iters += 1

            # Plot HCAs:
            if arguments.plot_dendrogram:
                print('\nGenerating dendrogram images. Please wait...')
                await MassaClusterService.hca_plot(linkage_bio, molecules_names, leaves_cluster_bio, CutOff_bio, 'bio',
                                    DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, arguments.dendrograms_x_axis_font_size,
                                    test_molecules, result_id, session)
                await MassaClusterService.hca_plot(linkage_phch, molecules_names, leaves_cluster_phch, CutOff_phch, 'PhCh',
                                    DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, arguments.dendrograms_x_axis_font_size,
                                    test_molecules, result_id, session)
                await MassaClusterService.hca_plot(linkage_fp, molecules_names, leaves_cluster_fp, CutOff_fp, 'FP',
                                    DefaultArgumentValues.DEFAULT_IMAGE_EXTENSION_TYPE, arguments.dendrograms_x_axis_font_size,
                                    test_molecules, result_id, session)

        

        result_service = ResultService(session)
        result = await result_service.get_result_by_id(result_id)
        return convert_result_to_images_output(result)
    except Exception as e:
        raise RuntimeError(f"Erro durante a execução: {e}")

    finally:
        # Limpeza do arquivo temporário
        if file_path and os.path.exists(file_path):
            os.remove(file_path)



def __calc_test_percentage(percentage_of_molecules_in_training_set: float) -> float:
    return round(float(1 - percentage_of_molecules_in_training_set), 3)

def __returns_zero(total, test):
    # It evaluates if the distribution is not adequate = the iterated cluster has a percentage greater than 0.5% in the complete data set, but a percentage lower than 0.5% in the test set.
    definer = False
    for i in total.keys():
        if (total[i] > 0.5) and (test[i] <= 0.5):
            definer = True # Definer = True (Distribution was not done properly).
    return definer