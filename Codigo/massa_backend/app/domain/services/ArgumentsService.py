from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.api.schemas.ArgumentsSchema import ArgumentsInput, ArgumentsOutput
from app.domain.models.ArgumentsModel import Arguments
from app.domain.models.mappers.ArgumentsMapper import convert_arguments_to_output
from app.infrastructure.repositories.ArgumentRepository import ArgumentsRepository


from sqlalchemy.future import select  # Import necessário para consultas no AsyncSession

class ArgumentsService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_arguments(self, arguments_data: dict) -> Arguments:
        arguments = Arguments(**arguments_data)
        try:
            self.session.add(arguments)
            await self.session.commit()
            return arguments  # Retorna o objeto criado
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Erro ao criar argumentos: {str(e)}")

    async def get_arguments_by_execution_id(self, execution_id: int) -> Arguments | None:
        try:
            result = await self.session.execute(
                select(Arguments).filter_by(execution_id=execution_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise RuntimeError(f"Erro ao buscar argumentos por execution_id: {str(e)}")

    async def update_arguments(self, arguments_id: int, arguments_data: ArgumentsInput):
        try:
            result = await self.session.execute(
                select(Arguments).filter_by(id=arguments_id)
            )
            arguments = result.scalars().first()

            if not arguments:
                raise RuntimeError("Arguments not found")

            # Atualiza os atributos do objeto
            for key, value in arguments_data.dict(exclude_unset=True).items():
                setattr(arguments, key, value)

            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RuntimeError(f"Erro ao atualizar argumentos: {str(e)}")

