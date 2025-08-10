# test_ExecutionService.py
import unittest
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from datetime import datetime, timedelta

from app.api.services.ExecutionService import ExecutionService
from app.domain.models.ExecutionModel import Execution, ExecutionStatus
from app.api.schemas.ExecutionSchema import ExecutionInput, ExecutionOutput
from app.api.schemas.ExecutionStatsSchema import ExecutionStatsInput


class TestExecutionService(unittest.TestCase):

    def setUp(self):
        self.mock_session = MagicMock()
        self.service = ExecutionService(self.mock_session)


    @patch('app.api.services.ExecutionService.ExecutionRepository')
    def test_create_execution(self, MockRepository):
        mock_repo = MockRepository.return_value
        data = ExecutionInput(user_id=1)
        expected_output = ExecutionOutput(id=1, user_id=1, start_time = datetime.now(), status=ExecutionStatus.IDLE)  # Example Output
        mock_repo.create.return_value = expected_output

        result = self.service.create_execution(data)

        mock_repo.create.assert_called_once_with(data)
        self.assertEqual(result, expected_output)

    def test_get_execution(self):
        execution_id = 1
        expected_execution = Execution(id=execution_id, user_id = 1) # Example Data
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = expected_execution

        result = self.service.get_execution(execution_id)

        self.assertEqual(result, expected_execution)

    @patch('app.api.services.ExecutionService.ExecutionRepository')
    def test_update_execution_success(self, MockRepository):
        mock_repo = MockRepository.return_value
        execution_id = 1
        data = ExecutionInput(user_id=2, status=ExecutionStatus.RUNNING)  # Example data
        updated_execution = ExecutionOutput(id=execution_id, user_id=2, start_time = datetime.now(), status=ExecutionStatus.RUNNING)   # Example updated data
        mock_repo.update.return_value = updated_execution

        result = self.service.update_execution(execution_id, data)

        self.assertEqual(result, updated_execution)
        mock_repo.update.assert_called_once_with(execution_id, data)

    @patch('app.api.services.ExecutionService.ExecutionRepository')
    def test_update_execution_not_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        execution_id = 1
        data = ExecutionInput(user_id=1) # Example data
        mock_repo.update.return_value = None

        with self.assertRaises(HTTPException) as context:
            self.service.update_execution(execution_id, data)

        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Execution not found")

    def test_update_execution_status_success(self):
        execution_id = 1
        execution = Execution(id=execution_id, status=ExecutionStatus.PENDING, user_id=1) # Example data
        self.mock_session.query.return_value.filter_by.return_value.first.return_value = execution
        self.mock_session.refresh = MagicMock()
        new_status = ExecutionStatus.COMPLETED

        result = self.service.update_execution_status(execution_id, new_status)

        self.assertEqual(result.status, new_status)
        self.mock_session.commit.assert_called_once()
        self.mock_session.refresh.assert_called_once_with(execution)


    def test_update_execution_status_not_found(self):
        execution_id = 999  # Nonexistent ID

        self.mock_session.query.return_value.filter_by.return_value.first.return_value = None

        with self.assertRaisesRegex(RuntimeError, "Execution not found"):
            self.service.update_execution_status(execution_id, ExecutionStatus.COMPLETED)



    @patch('app.api.services.ExecutionService.ExecutionRepository')
    @patch('app.api.services.ExecutionService.convert_output_to_execution')
    def test_delete_execution_success(self, mock_convert, MockRepository):

        mock_repo = MockRepository.return_value
        execution_id = 1
        mock_output = MagicMock()
        mock_execution = MagicMock()


        mock_repo.get_execution.return_value = mock_output
        mock_convert.return_value = mock_execution


        result = self.service.delete_execution(execution_id)


        mock_repo.get_execution.assert_called_once_with(execution_id)
        mock_convert.assert_called_once_with(mock_output)
        mock_repo.delete.assert_called_once_with(mock_execution)


    @patch('app.api.services.ExecutionService.ExecutionRepository')
    def test_delete_execution_not_found(self, MockRepository):

        mock_repo = MockRepository.return_value

        execution_id = 999

        mock_repo.get_execution.return_value = None



        with self.assertRaises(HTTPException) as context:
            self.service.delete_execution(execution_id)


        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Execution not found")