from datetime import timedelta

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncEngine

from app.api.routers.ExecutionRouter import ExecutionRouter
from app.api.routers.UserRouter import UserRouter
from app.api.routers.ExecutionStatsRouter import ExecutionStatsRouter
from app.core.Config import get_environment_variables
from app.domain.models.BaseModel import Base
from app.infrastructure.Database import async_engine
from app.domain.models import UserModel, ExecutionModel, ArgumentsModel, ExecutionStatsModel, ResultModel

env = get_environment_variables()

# Definição do lifespan corretamente implementado
async def lifespan(app: FastAPI):
    # Evento de startup
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield  # Ponto onde a aplicação executa
    # Evento de shutdown
    print("Encerrando a aplicação.")  # Aqui você pode adicionar lógica de limpeza, se necessário.

# Criação do app com ciclo de vida configurado
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    lifespan=lifespan,  # Define o ciclo de vida corretamente
)

# Configurações de middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registro de rotas
app.include_router(UserRouter)
app.include_router(ExecutionRouter)
app.include_router(ExecutionStatsRouter)
print(timedelta(3600))
