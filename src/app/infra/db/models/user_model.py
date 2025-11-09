# app/infrastructure/db/models/user_model.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infra.db.core import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
