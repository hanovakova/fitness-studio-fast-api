from sqlalchemy import ForeignKey, Boolean
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.orm_models.base import Base
from app.orm_models.user import User
from app.orm_models.fitness_class import FitnessClass

class UserClass(Base):
    """
    Represents the association between a User and a FitnessClass (many-to-many).
    Corresponds to the Java UserClass and UserClassKey.
    """
    __tablename__ = "user_classes"

    # Composite primary key made of two foreign keys
    userId: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    classId: Mapped[int] = mapped_column(ForeignKey("fitness_classes.id"), primary_key=True)

    # Extra data on the relationship
    paid: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships back to User and FitnessClass
    # These allow you to navigate from a UserClass object to its user or class
    user: Mapped["User"] = relationship(back_pop="class_associations")
    fitness_class: Mapped["FitnessClass"] = relationship(back_pop="user_associations")
