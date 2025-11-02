from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Float
from typing import List
from pydantic import EmailStr


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[EmailStr] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str]

    founds: Mapped[List["Found"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    first_name: Mapped[str] = mapped_column(String(30), nullable=True, default=None)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True, default=None)


class Found(Base):
    __tablename__ = "foundations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    desctiption: Mapped[str] = mapped_column(Text())
    goal: Mapped[float] = mapped_column(Float(2))
    current: Mapped[float] = mapped_column(Float(2))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="found")