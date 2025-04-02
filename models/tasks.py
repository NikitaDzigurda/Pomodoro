from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Tasks(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int]
    user_id: Mapped[int] = mapped_column(nullable=True)

    __table_args__ = {"extend_existing": True}


class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    type: Mapped[Optional[str]]

    __table_args__ = {"extend_existing": True}