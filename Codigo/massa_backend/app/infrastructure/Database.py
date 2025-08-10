from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
from ..core.Config import get_environment_variables

# Obter as variáveis de ambiente
env = get_environment_variables()

# URL do banco de dados assíncrono
ASYNC_DATABASE_URL = f"{env.DB_DIALECT}://{env.DB_USERNAME}:{env.DB_PASSWORD}@{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"

# Configurar o motor assíncrono
async_engine = create_async_engine(ASYNC_DATABASE_URL, echo=env.DEBUG_MODE)

# Criar uma fábrica de sessões assíncronas
AsyncSessionFactory = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Função para obter a sessão assíncrona
async def get_async_db_connection() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionFactory() as session:
        yield session
