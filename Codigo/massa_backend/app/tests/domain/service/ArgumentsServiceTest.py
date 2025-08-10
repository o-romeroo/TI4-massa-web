# test_ArgumentsService.py
import unittest
from unittest.mock import MagicMock, patch
from sqlalchemy.orm import scoped_session
from sqlalchemy.exc import SQLAlchemyError

from app.domain.services.ArgumentsService import ArgumentsService
from app.domain.models.ArgumentsModel import Arguments, SVDSolver, LinkageMethod
from app.api.schemas.ArgumentsSchema import ArgumentsInput


class TestArgumentsService(unittest.TestCase):

    def setUp(self):
        self.mock_session = MagicMock(spec=scoped_session)
        self.service = ArgumentsService(self.mock_session)

    @patch('app.domain.services.ArgumentsService.ArgumentsRepository')
    def test_create_arguments_success(self, MockRepository):
        mock_repo = MockRepository.return_value
        arguments_data = {"execution_id": 1, "biological_activities": ["activity1"], "percentage_of_molecules": 0.8,
                          "number_of_PCs": 3, "svd_solver_for_PCA": SVDSolver.FULL, "dendrograms_x_axis_font_size": 10,
                          "bar_plots_x_axis_font_size": 12, "linkage_method": LinkageMethod.WARD,
                          "plot_dendrogram": True}  # Example data
        created_arguments = Arguments(**arguments_data)
        mock_repo.session = self.mock_session
        mock_repo.session.add.return_value = None
        mock_repo.session.commit.return_value = None

        result = self.service.create_arguments(arguments_data)

        self.assertEqual(result, created_arguments)
        mock_repo.session.add.assert_called_once_with(created_arguments)
        mock_repo.session.commit.assert_called_once()

    @patch('app.domain.services.ArgumentsService.ArgumentsRepository')
    def test_create_arguments_failure(self, MockRepository):
        mock_repo = MockRepository.return_value
        arguments_data = {"execution_id": 1, "biological_activities": ["activity1"]}  # Example data
        mock_repo.session = self.mock_session
        mock_repo.session.add.side_effect = SQLAlchemyError("Database error")
        mock_repo.session.rollback.return_value = None

        with self.assertRaisesRegex(RuntimeError, "Erro ao criar argumentos: Database error"):
            self.service.create_arguments(arguments_data)

        mock_repo.session.rollback.assert_called_once()

    @patch('app.domain.services.ArgumentsService.ArgumentsRepository')
    def test_get_arguments_by_execution_id(self, MockRepository):
        mock_repo = MockRepository.return_value
        mock_repo.session = self.mock_session
        execution_id = 1
        expected_arguments = Arguments(execution_id=execution_id, biological_activities=["activity1"]) # Example data
        mock_repo.session.query.return_value.filter_by.return_value.first.return_value = expected_arguments

        result = self.service.get_arguments_by_execution_id(execution_id)

        self.assertEqual(result, expected_arguments)
        mock_repo.session.query.assert_called_once_with(Arguments)
        mock_repo.session.query.return_value.filter_by.assert_called_once_with(execution_id=execution_id)
        mock_repo.session.query.return_value.filter_by.return_value.first.assert_called_once()

    @patch('app.domain.services.ArgumentsService.ArgumentsRepository')
    def test_update_arguments_success(self, MockRepository):
        mock_repo = MockRepository.return_value
        mock_repo.session = self.mock_session

        arguments_id = 1
        arguments_data = ArgumentsInput(biological_activities=["new_activity"], percentage_of_molecules = 0.9)  # Example Data
        existing_arguments = Arguments(id=arguments_id, execution_id=1, biological_activities=["old_activity"], percentage_of_molecules = 0.1)  # Example Data

        mock_repo.session.query.return_value.get.return_value = existing_arguments

        self.service.update_arguments(arguments_id, arguments_data)

        self.assertEqual(existing_arguments.biological_activities, ["new_activity"])
        self.assertEqual(existing_arguments.percentage_of_molecules, 0.9)
        mock_repo.session.commit.assert_called_once()

    @patch('app.domain.services.ArgumentsService.ArgumentsRepository')
    def test_update_arguments_not_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        mock_repo.session = self.mock_session
        arguments_id = 1
        arguments_data = ArgumentsInput(biological_activities=["new_activity"])# Example Data
        mock_repo.session.query.return_value.get.return_value = None

        with self.assertRaisesRegex(RuntimeError, "Arguments not found"):
            self.service.update_arguments(arguments_id, arguments_data)

        mock_repo.session.commit.assert_not_called()