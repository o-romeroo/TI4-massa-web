import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.api.services.ExecutionStatsService import ExecutionStatsService
from app.api.schemas.ExecutionStatsSchema import ExecutionStatsInput, ExecutionStatsOutput



class TestExecutionStatsService(unittest.TestCase):

    def setUp(self):
        self.mock_session = MagicMock()
        self.service = ExecutionStatsService(self.mock_session)


    @patch('app.api.services.ExecutionStatsService.ExecutionStatsRepository')
    def test_create_stats(self, MockRepository):
        mock_repo = MockRepository.return_value
        data = ExecutionStatsInput(execution_id=1, molecule_count=100, biological_activity_count=5)  # Example data.
        expected_output = ExecutionStatsOutput(id=1, execution_id=1, molecule_count=100, biological_activity_count=5) # Example output
        mock_repo.create.return_value = expected_output


        result = self.service.create_stats(data)


        mock_repo.create.assert_called_once_with(data)
        self.assertEqual(result, expected_output)



    @patch('app.api.services.ExecutionStatsService.ExecutionStatsRepository')
    def test_get_stats_by_execution_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        execution_id = 1
        expected_stats =  ExecutionStatsOutput(id=1, execution_id=1, molecule_count=120, biological_activity_count=3)  # Example Data.
        mock_repo.get_stats_by_execution_id.return_value = expected_stats


        result = self.service.get_stats_by_execution(execution_id)


        self.assertEqual(result, expected_stats)
        mock_repo.get_stats_by_execution_id.assert_called_once_with(execution_id)




    @patch('app.api.services.ExecutionStatsService.ExecutionStatsRepository')
    def test_get_stats_by_execution_not_found(self, MockRepository):

        mock_repo = MockRepository.return_value

        execution_id = 1
        mock_repo.get_stats_by_execution_id.return_value = None


        with self.assertRaises(HTTPException) as context:
            self.service.get_stats_by_execution(execution_id)


        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "Stats not found")