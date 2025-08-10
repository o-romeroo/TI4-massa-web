from app.domain.models.UserModel import User
from app.api.schemas.UserSchema import UserOutput, CreateUserInput, UserLoginOutput


def convert_user_to_output(user: User) -> UserOutput:
    return UserOutput(
        id=user.id,
        username=user.username,
        email=user.email,
        country=user.country,
        city=user.city,
        is_active=user.is_active
    )

def convert_create_user_input_to_user(create_user_input: CreateUserInput) -> User:
    return User(
        username=create_user_input.username,
        email=create_user_input.email,
        password_hash=create_user_input.password,
        country=create_user_input.country,
        city=create_user_input.city
    )

def convert_output_to_user(user_output: UserOutput) -> User:
    return User(
        id=user_output.id,
        username=user_output.username,
        email=user_output.email,
        country=user_output.country,
        city=user_output.city
    )

def convert_user_to_user_login_output(user: User) -> UserLoginOutput:
    return UserLoginOutput(
        id=user.id,
        username=user.username,
        email=user.email,
        password_hash=user.password_hash
    )