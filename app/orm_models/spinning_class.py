from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.orm_models.fitness_class import FitnessClass


class SpinningClass(FitnessClass):
    """
    Represents a Spinning class.
    Corresponds to the Java SpinningClass model.
    """
    bikeType: Mapped[Optional[str]] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "spinning",  # Value for SpinningClass instances
    }

    def __repr__(self) -> str:
        return f"<SpinningClass(id={self.id!r}, name={self.name!r}, bike={self.bikeType!r})>"
