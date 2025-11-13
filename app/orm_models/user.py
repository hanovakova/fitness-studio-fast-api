from typing import Optional, List

from sqlalchemy import String, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.orm_models.base import Base
from app.orm_models.user_class import UserClass


class User(Base):
    """
    Represents a user of the fitness studio.
    Corresponds to the Java User model.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255)) # Hashed password
    name: Mapped[Optional[str]] = mapped_column(String(150))
    email: Mapped[Optional[str]] = mapped_column(String(150), unique=True, index=True)
    advertisement: Mapped[bool] = mapped_column(Boolean, default=False)
    avatarPath: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationship to the UserClass association object
    # From a User, you can get a list of their UserClass associations,
    # and from there, get the class itself and the paid status.
    class_associations: Mapped[List["UserClass"]] = relationship(
        back_pop="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, username={self.username!r})>"
