import datetime
from typing import Optional, List

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy import String, DateTime, Float
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


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
    start_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    end_time: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime)
    instructor_name: Mapped[Optional[str]] = mapped_column(String(100))
    price: Mapped[Optional[float]] = mapped_column(Float)
    capacity: Mapped[Optional[int]]
    image_path: Mapped[Optional[str]] = mapped_column(String(255))

    # --- Inheritance Configuration ---
    # This column will store the type of class (e.g., 'fitness', 'yoga', 'spinning')
    class_type: Mapped[str] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "fitness",  # Value for base class instances
        "polymorphic_on": "class_type",  # Column to check for type
    }

    # Relationship to the UserClass association object
    user_associations: Mapped[List["UserClass"]] = relationship(
        back_populates="fitness_class",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<FitnessClass(id={self.id!r}, name={self.name!r}, type={self.class_type!r})>"


class SpinningClass(FitnessClass):
    """
    Represents a Spinning class.
    Corresponds to the Java SpinningClass model.
    """
    bike_type: Mapped[Optional[str]] = mapped_column(String(100))

    __mapper_args__ = {
        "polymorphic_identity": "spinning",  # Value for SpinningClass instances
    }

    def __repr__(self) -> str:
        return f"<SpinningClass(id={self.id!r}, name={self.name!r}, bike={self.bike_type!r})>"


class User(Base):
    """
    Represents a user of the fitness studio.
    Corresponds to the Java User model.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(255))  # Hashed password
    name: Mapped[Optional[str]] = mapped_column(String(150))
    email: Mapped[Optional[str]] = mapped_column(String(150), unique=True, index=True)
    advertisement: Mapped[bool] = mapped_column(Boolean, default=False)
    avatar_path: Mapped[Optional[str]] = mapped_column(String(255))

    # Relationship to the UserClass association object
    # From a User, you can get a list of their UserClass associations,
    # and from there, get the class itself and the paid status.
    class_associations: Mapped[List["UserClass"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id!r}, username={self.username!r})>"


class UserClass(Base):
    """
    Represents the association between a User and a FitnessClass (many-to-many).
    Corresponds to the Java UserClass and UserClassKey.
    """
    __tablename__ = "user_classes"

    # Composite primary key made of two foreign keys
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    class_id: Mapped[int] = mapped_column(ForeignKey("fitness_classes.id"), primary_key=True)

    # Extra data on the relationship
    paid: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String, default="Pending")

    # Relationships back to User and FitnessClass
    # These allow you to navigate from a UserClass object to its user or class
    user: Mapped["User"] = relationship(back_populates="class_associations")
    fitness_class: Mapped["FitnessClass"] = relationship(back_populates="user_associations")


class YogaClass(FitnessClass):
    """
    Represents a Yoga class.
    Corresponds to the Java YogaClass model.
    """
    yoga_level: Mapped[Optional[str]] = mapped_column(String(50))

    __mapper_args__ = {
        "polymorphic_identity": "yoga",  # Value for YogaClass instances
    }

    def __repr__(self) -> str:
        return f"<YogaClass(id={self.id!r}, name={self.name!r}, level={self.yoga_level!r})>"
