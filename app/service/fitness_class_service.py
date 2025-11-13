from typing import List, Optional

from sqlalchemy import select, extract
from sqlalchemy.orm import Session

from app.config import SessionLocal
from app.orm_models.fitness_class import FitnessClass
from app.pydantic_models import FitnessClassCreate
from app.repository.fitness_class_repo import FitnessClassRepository
from app.service.transactions import run_in_transaction


class FitnessClassService:
    def __init__(self, repository: FitnessClassRepository):
        self.repo = repository

    @run_in_transaction(SessionLocal)
    def create_class(self, cl: FitnessClassCreate, session: Session) -> FitnessClass:
        """Service to create a new class. Handles transaction."""
        new_class = self.repo.create_fitness_class(session, cl.model_dump())
        return new_class

    @run_in_transaction(SessionLocal)
    def get_all_classes(self, session: Session) -> List[FitnessClass]:
        """Service to get all classes."""
        return self.repo.get_all_fitness_classes(session)

    @run_in_transaction(SessionLocal)
    def get_class_by_id(self, class_id: int, session: Session) -> FitnessClass:
        """Service to get a single class by ID."""
        db_class = self.repo.get_fitness_class(session, class_id=class_id)
        if not db_class:
            raise ValueError(f"Fitness class not found with ID: {class_id}")
        return db_class

    @run_in_transaction(SessionLocal)
    def get_filtered_classes(
            self,
            session: Session,
            time_frame: Optional[str] = None,
            class_type: Optional[str] = None
    ) -> List[FitnessClass]:
        """
        Filters classes in the database.
        """
        query = select(FitnessClass)
        if time_frame:
            time_frame = time_frame.lower()
            start_hour, end_hour = 0, 23
            if time_frame == "morning":
                start_hour, end_hour = 6, 12
            elif time_frame == "afternoon":
                start_hour, end_hour = 12, 18
            elif time_frame == "evening":
                start_hour, end_hour = 18, 23

            query = query.where(
                extract('hour', FitnessClass.startTime) >= start_hour,
                extract('hour', FitnessClass.startTime) < end_hour
            )
        if class_type:
            query = query.where(FitnessClass.class_type == class_type.lower())

        return list(session.scalars(query).all())

    def get_classes_by_time_frame(
            self, time_frame: str, classes: List[FitnessClass]
    ) -> List[FitnessClass]:
        """
        Filters a list of classes by time frame (pure Python logic).
        This matches the original Java service's in-memory filtering.
        """
        if not time_frame:
            return classes

        time_frame_lower = time_frame.lower()

        if time_frame_lower == "morning":
            start_hour, end_hour = 6, 12
        elif time_frame_lower == "afternoon":
            start_hour, end_hour = 12, 18
        elif time_frame_lower == "evening":
            start_hour, end_hour = 18, 23
        else:
            return classes  # Default: no filter if time is invalid

        def in_frame(c: FitnessClass):
            if not c.startTime:
                return False
            hour = c.startTime.hour
            return start_hour <= hour < end_hour

        return [c for c in classes if in_frame(c)]

    def get_classes_by_class_type(
            self, class_type: str, classes: List[FitnessClass]
    ) -> List[FitnessClass]:
        """
        Filters a list of classes by type (pure Python logic).
        This matches the original Java service's in-memory filtering.
        """
        if not class_type:
            return classes

        return [
            c for c in classes
            if c.class_type.lower() == class_type.lower()
        ]

    @run_in_transaction(SessionLocal)
    def is_class_capacity_exceeded(
            self, class_id: int, num_signed_up: int, session: Session
    ) -> bool:
        """
        Checks if a class is full, using a pessimistic lock.
        This matches the original Java service's logic.
        """
        fitness_class = self.repo.get_fitness_class_with_lock(session, class_id=class_id)
        if not fitness_class:
            raise ValueError(f"Fitness class not found with ID: {class_id}")

        if fitness_class.capacity is None:
            return False # No capacity limit

        return num_signed_up >= fitness_class.capacity
