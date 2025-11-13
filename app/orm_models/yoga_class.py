from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.orm_models.fitness_class import FitnessClass


class YogaClass(FitnessClass):
    """
    Represents a Yoga class.
    Corresponds to the Java YogaClass model.
    """
    yogaLevel: Mapped[Optional[str]] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "yoga",  # Value for YogaClass instances
    }

    def __repr__(self) -> str:
        return f"<YogaClass(id={self.id!r}, name={self.name!r}, level={self.yogaLevel!r})>"

