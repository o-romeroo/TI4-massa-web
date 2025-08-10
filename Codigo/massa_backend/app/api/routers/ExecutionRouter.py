from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
import os

from app.api.schemas.ArgumentsSchema import ArgumentsInput
from app.api.schemas.ExecutionSchema import ExecutionOutput, ExecutionInput
from app.api.schemas.ExecutionStatsSchema import ExecutionStatsInput
from app.api.schemas.ResultSchema import ResultStartOutput, ImagesOutput, ResultInput
from app.api.schemas.UserSchema import UserOutput
from app.domain.models.ExecutionModel import ExecutionStatus
from app.domain.models.mappers.ResultMapper import convert_result_to_images_output
from app.domain.services.ArgumentsService import ArgumentsService
from app.domain.services.ExecutionService import ExecutionService
from app.domain.services.ExecutionStatsService import ExecutionStatsService
from app.domain.services.ResultService import ResultService, generate_pdf_from_images
from app.domain.services.massa.MassaExtractionService import get_molecules_count
from app.domain.services.massa.MassaReaderService import get_sdf_property_names, read_SDF
from app.helpers import FileUtils
from app.infrastructure.Database import get_async_db_connection

from app.domain.services.massa.MassaService import execute, executeGraphic
from app.domain.models.ArgumentsModel import Arguments, LinkageMethod, SVDSolver
from app.domain.constants import DefaultArgumentValues
from app.core.Security import JWTAuth

ExecutionRouter = APIRouter(
    prefix="/executions",
    tags=["execution"]
)

jwt_auth = JWTAuth()

@ExecutionRouter.post("/create", status_code=201, summary="Create Execution (Step 1)")
async def create_execution(
    current_user: UserOutput = Depends(jwt_auth.get_current_user),
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_async_db_connection)
) -> dict:
    _service = ExecutionService(session)
    arguments_service = ArgumentsService(session)
    file_path = None

    try:
        print("Expiring all sessions...")
        session.expire_all()  # Não precisa de await

        print(f"Validating file extension for: {file.filename}")
        if not any(file.filename.endswith(ext) for ext in [".mol2", ".sdf", ".mol", ".xls", ".xlsx", ".csv"]):
            raise HTTPException(status_code=400, detail="The file must be one of the following types: .mol2, .sdf, .mol, .xls, .xlsx, .csv")

        print("Creating temporary file...")
        file_path = await FileUtils.create_temp_file(file)
        print(f"Temporary file created at: {file_path}")

        print("Reading sanitized molecules...")
        sanitized_molecules = read_SDF(file_path)  # Remova o await se `read_SDF` for síncrona
        print("Sanitized molecules read successfully.")

        print("Getting SDF property names...")
        sdf_property_names = get_sdf_property_names(sanitized_molecules)  # Remova o await se `get_sdf_property_names` for síncrona
        print(f"SDF Property Names: {sdf_property_names}")

        print("Creating execution input...")
        execution_data = ExecutionInput(user_id=current_user.id)
        execution = await _service.create_execution(execution_data)
        print(f"Execution created with ID: {execution.id}")

        print("Creating arguments data...")
        arguments_data = ArgumentsInput(
            execution_id=execution.id,
            biological_activities=sdf_property_names,
        )
        arguments_dict = arguments_data.model_dump(exclude_none=True)
        await arguments_service.create_arguments(arguments_dict)
        await session.commit()
        print("Arguments committed successfully.")

        return {"arguments": arguments_dict}

    except Exception as e:
        print(f"Error processing file: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    finally:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Temporary file removed: {file_path}")
            except Exception as remove_error:
                print(f"Error removing temporary file: {remove_error}")



@ExecutionRouter.put("/update", status_code=200, summary="Update Arguments and Execution Status (Step 2)")
async def update_arguments_and_status(
    arguments_data: ArgumentsInput,
    session: AsyncSession = Depends(get_async_db_connection),
):
    execution_service = ExecutionService(session)
    arguments_service = ArgumentsService(session)

    status = ExecutionStatus.PROCESSING

    try:
        # Buscar a execução pelo ID
        execution = await execution_service.get_execution(arguments_data.execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        # Buscar os argumentos pelo ID da execução
        arguments = await arguments_service.get_arguments_by_execution_id(arguments_data.execution_id)
        if not arguments:
            raise HTTPException(status_code=404, detail="Arguments not found for this Execution")

        # Atualizar argumentos
        await arguments_service.update_arguments(arguments.id, arguments_data)

        # Atualizar status da execução
        execution_update_data = ExecutionInput(
            id=execution.id,
            user_id=execution.user_id,
            status=status,
            end_time=None,  # Atualize conforme a lógica do seu caso
        )
        await execution_service.update_execution(execution.id, execution_update_data)

        # Confirma as mudanças no banco
        await session.commit()

        return {"message": "Execution Status and Arguments updated successfully"}

    except HTTPException as e:
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating Execution and Arguments: {str(e)}")



@ExecutionRouter.post("/start", status_code=200, summary="Start Algorithm Execution (Step 3)")
async def start_execution(
    execution_id: int,
    file: UploadFile,
    session: AsyncSession = Depends(get_async_db_connection),
):
    execution_service = ExecutionService(session)
    arguments_service = ArgumentsService(session)
    result_service = ResultService(session)
    stats_service = ExecutionStatsService(session)

    status = ExecutionStatus.FINISHED

    try:
        # Expira todas as sessões no início
        await session.rollback()  # Certifica-se de que a sessão está limpa

        # Verifica a execução
        execution = await execution_service.get_execution(execution_id)
        if not execution:
            raise HTTPException(status_code=404, detail="Execution not found")

        # Busca os argumentos
        db_arguments = await arguments_service.get_arguments_by_execution_id(execution_id)
        if not db_arguments:
            raise HTTPException(status_code=404, detail="Arguments not found for this Execution")

        # Constrói o objeto Arguments
        arguments = Arguments(
            number_of_PCs=db_arguments.number_of_PCs,
            svd_solver_for_PCA=db_arguments.svd_solver_for_PCA.value if isinstance(db_arguments.svd_solver_for_PCA, SVDSolver) else db_arguments.svd_solver_for_PCA,
            dendrograms_x_axis_font_size=db_arguments.dendrograms_x_axis_font_size,
            bar_plots_x_axis_font_size=db_arguments.bar_plots_x_axis_font_size,
            linkage_method=db_arguments.linkage_method.value if isinstance(db_arguments.linkage_method, LinkageMethod) else db_arguments.linkage_method,
            plot_dendrogram=db_arguments.plot_dendrogram,
            biological_activities=db_arguments.biological_activities,
            percentage_of_molecules=db_arguments.percentage_of_molecules,
        )

        # Cria o resultado
        result = await result_service.create_result(ResultInput(execution_id=execution_id))
        if not result:
            raise RuntimeError("Failed to create result entry.")

        # Executa o gráfico
        graphics = await executeGraphic(arguments=arguments, result_id=result.id, session=session, file=file)
        if not graphics:
            raise RuntimeError("Failed to generate graphics.")

         
        await file.seek(0)
        molecules_count = await get_molecules_count(file)

        # Cria as estatísticas de execução
        registered_execution_stats = ExecutionStatsInput(
            execution_id=execution_id,
            molecule_count=molecules_count,
            biological_activity_count=len(arguments.biological_activities),
        )
        stats = await stats_service.create_stats(data=registered_execution_stats)

        # Atualiza o status da execução
        execution_input = ExecutionInput(
            id=execution_id,
            user_id=execution.user_id,
            status=status,
            end_time=datetime.now(),
        )
        await execution_service.update_execution(execution_id, execution_input)

        # Confirma as mudanças no banco
        await session.commit()

        return ResultStartOutput(
            message="Analysis executed successfully",
            images=graphics,
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error executing analysis: {str(e)}")



@ExecutionRouter.get("/{execution_id}", status_code=200, response_model=ExecutionOutput)
async def get_execution(execution_id: int, session: AsyncSession = Depends(get_async_db_connection)) -> ExecutionOutput:
    _service = ExecutionService(session)
    execution = await _service.get_execution(execution_id)

    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")

    return execution


@ExecutionRouter.get("/images/{result_id}", status_code=200, response_model=ImagesOutput)
async def get_plotted_images(result_id: int, session: AsyncSession = Depends(get_async_db_connection)) -> ImagesOutput:
    _service = ResultService(session)
    return await convert_result_to_images_output(await _service.get_result_by_id(result_id))


@ExecutionRouter.post("/execute")
async def test1_execution(
    result_id: int,
    file: UploadFile,
    session: AsyncSession = Depends(get_async_db_connection)
):
    arguments = Arguments(
        number_of_PCs=DefaultArgumentValues.DEFAULT_NUMBER_OF_PCS,
        svd_solver_for_PCA=SVDSolver.FULL.value,
        dendrograms_x_axis_font_size=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_DENDROGRAMS,
        bar_plots_x_axis_font_size=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_BAR_PLOTS,
        linkage_method=LinkageMethod.COMPLETE.value,
        plot_dendrogram=True,
        biological_activities=["ACTIVITY"],
        percentage_of_molecules=DefaultArgumentValues.DEFAULT_PERCENTAGE_OF_MOLECULES
    )

    try:
        returned_images = await execute(arguments=arguments, result_id=result_id, session=session, file=file)
        return ResultStartOutput(
            message="Analysis executed successfully",
            images=returned_images
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ExecutionRouter.post("/executeGraphic")
async def test2_execution(
    result_id: int,
    file: UploadFile,
    session: AsyncSession = Depends(get_async_db_connection)
):
    arguments = Arguments(
        number_of_PCs=DefaultArgumentValues.DEFAULT_NUMBER_OF_PCS,
        svd_solver_for_PCA=SVDSolver.FULL.value,
        dendrograms_x_axis_font_size=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_DENDROGRAMS,
        bar_plots_x_axis_font_size=DefaultArgumentValues.DEFAULT_FONT_FOR_X_AXIS_OF_BAR_PLOTS,
        linkage_method=LinkageMethod.COMPLETE.value,
        plot_dendrogram=True,
        biological_activities=["ACTIVITY"],
        percentage_of_molecules=DefaultArgumentValues.DEFAULT_PERCENTAGE_OF_MOLECULES
    )

    try:
        returned_images = await executeGraphic(arguments=arguments, result_id=result_id, session=session, file=file)
        return returned_images

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@ExecutionRouter.get("/download-pdf/{execution_id}", summary="Download Result as PDF")
async def download_pdf(
    execution_id: int,
    session: AsyncSession = Depends(get_async_db_connection)
):
    result_service = ResultService(session)

    try:
        result = await result_service.get_result_by_execution_id(execution_id)
    except HTTPException as e:
        raise e

    pdf_buffer = None
    try:
        pdf_buffer = await generate_pdf_from_images(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate PDF: {str(e)}")

    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=result_MASSA.pdf"}
    )
