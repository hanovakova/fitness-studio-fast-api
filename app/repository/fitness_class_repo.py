from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm_models.fitness_class import FitnessClass

class FitnessClassRepository:

    def get_fitness_class(self, session: Session, class_id: int) -> Optional[ FitnessClass]:
        """Gets a single fitness class by its ID."""
        return session.get(FitnessClass, class_id)

    def get_all_fitness_classes(self, session: Session, skip: int = 0, limit: int = 100) -> List[ FitnessClass]:
        """Gets a list of all fitness classes with pagination."""
        statement = select( FitnessClass).offset(skip).limit(limit)
        return list(session.scalars(statement).all())

    def get_fitness_class_with_lock(self, session: Session, class_id: int) -> Optional[ FitnessClass]:
        """
        Gets a single fitness class by ID with a PESSIMISTIC WRITE lock.
        Replicates findByIdWithLock.
        For PostgreSQL, this translates to "FOR UPDATE".
        """
        return session.get(FitnessClass, class_id, with_for_update=True)

    def create_fitness_class(self, session: Session, cl_data: dict) -> FitnessClass:
        db_fitness_class = FitnessClass(**cl_data)
        session.add(db_fitness_class)
        session.commit()
        session.refresh(db_fitness_class)
        return db_fitness_class
