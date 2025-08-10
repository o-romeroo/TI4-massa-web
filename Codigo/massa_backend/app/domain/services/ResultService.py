from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from PIL import Image
import base64

from app.api.schemas.ResultSchema import ImagesOutput, ResultInput, ResultOutput
from app.domain.models.ResultModel import ResultModel
from app.domain.models.mappers.ResultMapper import convert_result_to_images_output
from app.infrastructure.repositories.ResultRepository import ResultRepository


class ResultService:

    def __init__(self, session: AsyncSession):
        self.repository = ResultRepository(session)

    async def create_result(self, data: ResultInput) -> ResultOutput:
        try:
            return await self.repository.create(data)
        except SQLAlchemyError as e:
            await self.repository.session.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating result: {str(e)}")

    async def get_result_by_id(self, result_id: int) -> ResultModel:
        result = await self.repository.get_by_id(result_id)

        if not result:
            raise HTTPException(status_code=404, detail="Result not found")

        return result

    async def get_result_by_execution_id(self, execution_id: int) -> ResultModel:
        result = await self.repository.get_result_by_execution_id(execution_id)
        if not result:
            raise HTTPException(status_code=404, detail="Result not found for this Execution")
        return result

    async def get_plotted_graphics_by_id(self, result_id: int) -> ImagesOutput:
        result = await self.repository.get_by_id(result_id)

        if not result:
            raise HTTPException(status_code=404, detail="Result not found")

        return result

    async def update_result(self, result_id: int, column_table: str, buffer: BytesIO):
        # Converte o buffer em bytes (BLOB)
        blob_data = buffer.getvalue()

        # Atualiza a coluna específica do resultado com o BLOB
        try:
            result = await self.repository.update_column(result_id, column_table, blob_data)

            if not result:
                raise HTTPException(status_code=404, detail="Result not found")

            return result
        except SQLAlchemyError as e:
            await self.repository.session.rollback()
            raise HTTPException(status_code=500, detail="An error occurred while updating the result.")


async def generate_pdf_from_images(result: ResultModel) -> BytesIO:
    pdf_buffer = BytesIO()

    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    page_width, page_height = letter

    img_width = page_width * 0.9
    img_height = page_height * 0.45

    x = (page_width - img_width) / 2
    y_top = page_height - 50
    y_bottom = y_top - img_height - 20

    images_per_page = 2
    image_counter = 0

    def add_images_to_pdf(images_dict):
        nonlocal image_counter, y_top, y_bottom
        if not images_dict:
            return

        for image_name, image_base64 in images_dict.items():
            if image_base64:
                try:
                    image_data = base64.b64decode(image_base64)
                    image_stream = BytesIO(image_data)

                    img = Image.open(image_stream)

                    img_reader = ImageReader(img)

                    y = y_top if image_counter % images_per_page == 0 else y_bottom

                    c.drawImage(img_reader, x, y - img_height, width=img_width, height=img_height)

                    image_counter += 1

                    if image_counter % images_per_page == 0:
                        c.showPage()
                        y_top = page_height - 50
                        y_bottom = y_top - img_height - 20

                except Exception as e:
                    print(f"Error adding image {image_name} to PDF: {e}")
            else:
                print(f"No data for image: {image_name}")

    images_output = convert_result_to_images_output(result)
    add_images_to_pdf(images_output.dendrograms)
    add_images_to_pdf(images_output.distance_plots)
    add_images_to_pdf(images_output.distribution_plots)

    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer
