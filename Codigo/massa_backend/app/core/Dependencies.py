from typing import Type, Callable, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.Database import get_async_db_connection

T = TypeVar("T")

def get_repository(repo_type: Type[T]) -> Callable[[], T]:

    def get_repo(session: AsyncSession = Depends(get_async_db_connection)):
        return repo_type(session)

    return get_repo