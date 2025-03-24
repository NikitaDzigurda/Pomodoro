from database import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserProfile(Base):
    __tablename__ = "userprofile"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    access_token: Mapped[str] = mapped_column(nullable=False)
