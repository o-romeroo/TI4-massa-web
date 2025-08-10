import unittest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
import uuid

from app.api.services.UserService import UserService
from app.api.schemas.UserSchema import UserInput, UserOutput, CreateUserOutput


class TestUserService(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.service = UserService(self.mock_session)

    @patch('app.api.services.UserService.UserRepository')
    @patch('app.api.services.UserService.JWTAuth')
    def test_create_user(self, MockJWTAuth, MockRepository):
        mock_repo = MockRepository.return_value
        mock_auth = MockJWTAuth.return_value
        data = UserInput(session_id=str(uuid.uuid4()), country="US", city="New York") # Example Data
        created_user = MagicMock()
        created_user.id = 1
        created_user.session_id = data.session_id
        mock_repo.create.return_value = created_user
        mock_auth.create_access_token.return_value = "test_token"


        result = self.service.create_user(data)


        mock_repo.create.assert_called_once_with(data)
        mock_auth.create_access_token.assert_called_once_with(created_user.id)
        self.assertEqual(result, CreateUserOutput(session_id=data.session_id, token="test_token"))

    @patch('app.api.services.UserService.UserRepository')
    def test_get_user_found(self, MockRepository):
        mock_repo = MockRepository.return_value
        user_id = 1
        expected_user = UserOutput(id=user_id, session_id=str(uuid.uuid4()), country="BR", city="São Paulo") # Example User
        mock_repo.get_user.return_value = expected_user



        result = self.service.get_user(user_id)



        self.assertEqual(result, expected_user)

        mock_repo.get_user.assert_called_once_with(user_id)





    @patch('app.api.services.UserService.UserRepository')
    def test_get_user_not_found(self, MockRepository):

        mock_repo = MockRepository.return_value


        user_id = 1


        mock_repo.get_user.return_value = None




        with self.assertRaises(HTTPException) as context:
            self.service.get_user(user_id)


        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "User not found")




    @patch('app.api.services.UserService.UserRepository')
    @patch('app.api.services.UserService.convert_input_to_user')
    def test_update_user_success(self, mock_convert, MockRepository):

        mock_repo = MockRepository.return_value


        data = UserInput(session_id=str(uuid.uuid4()), country="UK", city="London") # Example data

        user_id = 1
        mock_user = MagicMock()


        updated_user = UserOutput(id=user_id, session_id=data.session_id, country=data.country, city=data.city) # Example updated user

        mock_convert.return_value = mock_user

        mock_repo.update.return_value = updated_user




        result = self.service.update_user(data, user_id)




        mock_convert.assert_called_once_with(data)

        mock_repo.update.assert_called_once_with(mock_user, user_id)

        self.assertEqual(result, updated_user)





    @patch('app.api.services.UserService.UserRepository')
    @patch('app.api.services.UserService.convert_input_to_user')
    def test_update_user_not_found(self, mock_convert, MockRepository):

        mock_repo = MockRepository.return_value



        data = UserInput(session_id=str(uuid.uuid4()), country="CA", city="Toronto") # Example data

        user_id = 1
        mock_user = MagicMock()

        mock_convert.return_value = mock_user




        mock_repo.update.return_value = None




        with self.assertRaises(HTTPException) as context:
            self.service.update_user(data, user_id)



        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "User not found")




    @patch('app.api.services.UserService.UserRepository')
    @patch('app.api.services.UserService.convert_output_to_user')
    def test_delete_user_success(self, mock_convert, MockRepository):
        mock_repo = MockRepository.return_value
        user_id = 1

        mock_output = MagicMock()

        mock_repo.get_user.return_value = mock_output


        mock_user = MagicMock()

        mock_convert.return_value = mock_user


        mock_repo.delete.return_value = True




        result = self.service.delete_user(user_id)




        self.assertTrue(result)


        mock_repo.get_user.assert_called_once_with(user_id)
        mock_convert.assert_called_once_with(mock_output)
        mock_repo.delete.assert_called_once_with(mock_user)





    @patch('app.api.services.UserService.UserRepository')
    def test_delete_user_not_found(self, MockRepository):
        mock_repo = MockRepository.return_value

        user_id = 1

        mock_repo.get_user.return_value = None



        with self.assertRaises(HTTPException) as context:
            self.service.delete_user(user_id)



        self.assertEqual(context.exception.status_code, 404)
        self.assertEqual(context.exception.detail, "User not found")