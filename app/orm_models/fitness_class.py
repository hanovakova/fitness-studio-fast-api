import datetime
from typing import Optional, List

from sqlalchemy import String, DateTime, Float
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.orm_models.base import Base
from app.orm_models.user_class import UserClass


class FitnessClass(Base):
    """
    Base model for all fitness classes.
    Corresponds to the Java FitnessClass model.
    Implements Single Table Inheritance.
    """
    __tablename__ = "fitness_classes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(150))
    description: Mapped[Optional[str]]
    startTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    endTime: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    instructorName: Mapped[Optional[str]] = mapped_column(String(100))
    price: Mapped[Optional[float]] = mapped_column(Float)
    capacity: Mapped[Optional[int]]
    imagePath: Mapped[Optional[str]] = mapped_column(String(255))

    # --- Inheritance Configuration ---
    # This column will store the type of class (e.g., 'fitness', 'yoga', 'spinning')
    class_type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "fitness",  # Value for base class instances
        "polymorphic_on": "class_type",  # Column to check for type
    }

    # Relationship to the UserClass association object
    user_associations: Mapped[List["UserClass"]] = relationship(
        back_pop="fitness_class",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<FitnessClass(id={self.id!r}, name={self.name!r}, type={self.class_type!r})>"
