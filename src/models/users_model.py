from datetime import datetime, timezone
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, Boolean, TIMESTAMP, Enum, func
from sqlalchemy import ForeignKey, Integer

from sqlalchemy.orm import Mapped, mapped_column, declarative_base
from src.auth.api_key import default_expiry_date

UserBase = declarative_base()


class User(UserBase):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    company_name: Mapped[str] = mapped_column(String, index=True, nullable=False, default='new_user')


class AccessToken(UserBase):
    __tablename__ = "api_token"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False)
    api_token: Mapped[str] = mapped_column(String(length=150), nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    expired_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=default_expiry_date)
