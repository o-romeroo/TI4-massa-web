from typing import List

from sqlalchemy import Integer, String, UUID, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.domain.models.BaseModel import Base

from app.domain.models.ExecutionModel import Execution

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(96))
    country: Mapped[str] = mapped_column(String(120))
    city: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    executions: Mapped[List["Execution"]] = relationship()

