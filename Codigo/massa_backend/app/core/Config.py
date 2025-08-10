import os
from pydantic_settings import BaseSettings

def get_env_filename():
    return os.environ.get("ENV_FILE")

class EnvironmentSettings(BaseSettings):
    APP_NAME: str
    API_VERSION: str
    DB_DIALECT: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DEBUG_MODE: bool
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_EXP_DELTA_SECONDS: int

    class Config:
        env_file = get_env_filename()

def get_environment_variables():
    return EnvironmentSettings()