from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Text, Float, CheckConstraint, DateTime
from typing import List
from pydantic import EmailStr
from datetime import datetime


class Base(DeclarativeBase): pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str]

    balance: Mapped[int] = mapped_column(Float(2), default=0)
    first_name: Mapped[str] = mapped_column(String(30), nullable=True, default=None)
    last_name: Mapped[str] = mapped_column(String(30), nullable=True, default=None)

    founds: Mapped[List["Found"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    
    __table_args__ = (
        CheckConstraint('balance >= 0', name='check_balance_positive'),
    )


class Found(Base):
    __tablename__ = "foundations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(Text())
    goal: Mapped[float] = mapped_column(Float(2)) 
    current: Mapped[float] = mapped_column(Float(2), default=0)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="founds")

    __table_args__ = (
        CheckConstraint('current >= 0', name='check_current_positive'),
        CheckConstraint('goal > 0', name='check_goal_positive'),
    )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(Float(2)) 
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    found_id: Mapped[int] = mapped_column(ForeignKey("foundations.id"), nullable=False)





