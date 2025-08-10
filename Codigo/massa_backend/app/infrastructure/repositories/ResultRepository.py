from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.api.schemas.ResultSchema import ResultInput, ResultOutput
from app.domain.models.mappers.ResultMapper import convert_result_to_output
from app.domain.models.ResultModel import ResultModel


class ResultRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: ResultInput) -> ResultOutput:
        result = ResultModel(**data.dict())
        try:
            self.session.add(result)
            await self.session.commit()
            await self.session.refresh(result)
            return convert_result_to_output(result)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating result: {str(e)}")

    async def get_result_by_execution_id(self, execution_id: int) -> Optional[ResultModel]:
        result = await self.session.execute(
            select(ResultModel).where(ResultModel.execution_id == execution_id)
        )
        return result.scalars().first()

    async def get_all(self) -> List[Optional[ResultOutput]]:
        results = await self.session.execute(select(ResultModel))
        response: List[ResultOutput] = []
        for result in results.scalars():
            response.append(convert_result_to_output(result))
        return response

    async def get_by_id(self, result_id: int) -> Optional[ResultOutput]:
        result = await self.session.execute(
            select(ResultModel).where(ResultModel.id == result_id)
        )
        result = result.scalars().first()
        if result:
            return convert_result_to_output(result)
        return None

    async def update(self, result_id: int, data: ResultInput) -> Optional[ResultOutput]:
        result = await self.session.execute(
            select(ResultModel).where(ResultModel.id == result_id)
        )
        result_updt = result.scalars().first()

        if not result_updt:
            return None

        # Atualiza os atributos
        result_updt.biological_hca_euclidian_distances = data.biological_hca_euclidian_distances
        result_updt.physicochemical_hca_euclidian_distances = data.physicochemical_hca_euclidian_distances
        result_updt.structural_hca_euclidian_distances = data.structural_hca_euclidian_distances
        result_updt.biological_clustering_dataset_dist = data.biological_clustering_dataset_dist
        result_updt.structural_clustering_dataset_dist = data.structural_clustering_dataset_dist
        result_updt.physicochemical_clustering_dataset_dist = data.physicochemical_clustering_dataset_dist
        result_updt.general_clustering_dataset_dist = data.general_clustering_dataset_dist
        result_updt.biological_activity_hca = data.biological_activity_hca
        result_updt.physicochemical_properties_hca = data.physicochemical_properties_hca
        result_updt.atom_pairs_fingerprint_hca = data.atom_pairs_fingerprint_hca

        try:
            await self.session.commit()
            await self.session.refresh(result_updt)
            return convert_result_to_output(result_updt)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating result: {str(e)}")

    async def update_column(self, result_id: int, column_table: str, blob_data: bytes) -> Optional[ResultOutput]:
        try:
            result = await self.session.execute(
                select(ResultModel).where(ResultModel.id == result_id)
            )
            result_updt = result.scalars().first()

            if not result_updt:
                raise HTTPException(status_code=404, detail="Result not found")

            if hasattr(result_updt, column_table):
                setattr(result_updt, column_table, blob_data)
            else:
                raise AttributeError(f"Column {column_table} does not exist in ResultModel.")

            await self.session.commit()
            await self.session.refresh(result_updt)
            return convert_result_to_output(result_updt)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating column: {str(e)}")
