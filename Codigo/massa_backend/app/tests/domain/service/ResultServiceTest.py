# test_ResultService.py
import unittest
from unittest.mock import MagicMock, patch, mock_open
from io import BytesIO
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from PIL import Image
from reportlab.lib.pagesizes import letter # Import letter explicitly


from app.api.services.ResultService import ResultService
from app.domain.models.ResultModel import ResultModel
from app.api.schemas.ResultSchema import ResultInput, ResultOutput, ImagesOutput, GraphicsOutput, DistancePlotsOutput, DistributionPlotsOutput


class TestResultService(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.service = ResultService(self.mock_session)


        # Example of base64 encoded image
        self.example_base64_image = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
        self.mock_result = ResultModel(
            execution_id=1,
            dendrogram_ward=self.example_base64_image,
            dendrogram_complete=self.example_base64_image,
            dendrogram_average=self.example_base64_image,
            dendrogram_single=self.example_base64_image,
            distance_plot_complete=self.example_base64_image,
            distance_plot_average=self.example_base64_image,
            distance_plot_ward=self.example_base64_image,
            distance_plot_single=self.example_base64_image,
            distribution_plot_by_execution_time=self.example_base64_image,
            distribution_plot_by_number_of_methods=self.example_base64_image,
        )


    @patch('app.api.services.ResultService.ResultRepository')
    def test_create_result(self, MockRepository):
        mock_repo = MockRepository.return_value
        data = ResultInput(execution_id=1)
        expected_output = ResultOutput(id=1, execution_id=1)
        mock_repo.create.return_value = expected_output

        result = self.service.create_result(data)

        mock_repo.create.assert_called_once_with(data)
        self.assertEqual(result, expected_output)


    @patch('app.api.services.ResultService.ResultRepository')
    def test_get_result_by_id_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        result_id = 1
        mock_repo.get_by_id.return_value = self.mock_result

        result = self.service.get_result_by_id(result_id)

        self.assertEqual(result, self.mock_result)
        mock_repo.get_by_id.assert_called_once_with(result_id)

    @patch('app.api.services.ResultService.ResultRepository')
    def test_get_result_by_id_not_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        result_id = 1
        mock_repo.get_by_id.return_value = None

        with self.assertRaises(HTTPException) as context:
            self.service.get_result_by_id(result_id)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Result not found")

    @patch('app.api.services.ResultService.ResultRepository')
    def test_get_result_by_execution_id_found(self, MockRepository):

        mock_repo = MockRepository.return_value
        execution_id = 1
        mock_repo.get_result_by_execution_id.return_value = self.mock_result


        result = self.service.get_result_by_execution_id(execution_id)


        self.assertEqual(result, self.mock_result)
        mock_repo.get_result_by_execution_id.assert_called_once_with(execution_id)


    @patch('app.api.services.ResultService.ResultRepository')
    def test_get_result_by_execution_id_not_found(self, MockRepository):

        mock_repo = MockRepository.return_value

        execution_id = 1

        mock_repo.get_result_by_execution_id.return_value = None



        with self.assertRaises(HTTPException) as context:
            self.service.get_result_by_execution_id(execution_id)



        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Result not found for this Execution")



    @patch('app.api.services.ResultService.ResultRepository')
    def test_get_plotted_graphics_by_id_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        result_id = 1

        mock_repo.get_by_id.return_value = self.mock_result



        result = self.service.get_plotted_graphics_by_id(result_id)




        self.assertEqual(result, self.mock_result)

        mock_repo.get_by_id.assert_called_once_with(result_id)






    @patch('app.api.services.ResultService.ResultRepository')
    def test_get_plotted_graphics_by_id_not_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        result_id = 1

        mock_repo.get_by_id.return_value = None



        with self.assertRaises(HTTPException) as context:
            self.service.get_plotted_graphics_by_id(result_id)


        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Result not found")




    @patch('app.api.services.ResultService.ResultRepository')
    def test_update_result_success(self, MockRepository):
        mock_repo = MockRepository.return_value
        result_id = 1
        column_table = "test_column"
        buffer = BytesIO(b"test data")

        mock_repo.update_column.return_value = self.mock_result

        result = self.service.update_result(result_id, column_table, buffer)


        self.assertEqual(result, self.mock_result)

        mock_repo.update_column.assert_called_once_with(result_id, column_table, buffer.getvalue())



    @patch('app.api.services.ResultService.ResultRepository')
    def test_update_result_not_found(self, MockRepository):

        mock_repo = MockRepository.return_value

        result_id = 1
        column_table = "test_column"
        buffer = BytesIO(b"test data")


        mock_repo.update_column.return_value = None




        with self.assertRaises(HTTPException) as context:
            self.service.update_result(result_id, column_table, buffer)


        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Result not found")



    @patch('app.api.services.ResultService.ResultRepository')
    def test_update_result_error(self, MockRepository):

        mock_repo = MockRepository.return_value

        result_id = 1
        column_table = "test_column"
        buffer = BytesIO(b"test data")

        mock_repo.update_column.side_effect = SQLAlchemyError("Database error")




        with self.assertRaises(HTTPException) as context:
            self.service.update_result(result_id, column_table, buffer)


        self.assertEqual(context.exception.status_code, 500)
        self.assertEqual(context.exception.detail, "An error occurred while updating the result.")




    @patch("app.api.services.ResultService.canvas.Canvas")
    @patch("app.api.services.ResultService.convert_result_to_images_output")
    @patch("builtins.open", new_callable=mock_open)  # Mock 'open' built-in function
    def test_generate_pdf_from_images(self, mock_file, mock_convert, MockCanvas):
        # Setup
        mock_canvas = MockCanvas.return_value
        mock_file.return_value = MagicMock()

        example_images_output = ImagesOutput(
            dendrograms={"test": self.example_base64_image},
            distance_plots={"test": self.example_base64_image},
            distribution_plots={"test": self.example_base64_image},
        )
        mock_convert.return_value = example_images_output

        pdf_file_path = "test.pdf"



        # Execution

        self.service.generate_pdf_from_images(self.mock_result, pdf_file_path)



        # Assertions
        MockCanvas.assert_called_once_with(pdf_file_path, pagesize=letter)
        mock_canvas.save.assert_called_once()