from typing import Optional

from sqlalchemy.orm import Session, with_polymorphic
from sqlalchemy.orm.util import AliasedClass

from app.orm_models import FitnessClass


class FitnessClassRepository:

    def get_fitness_class(self, session: Session, class_id: int) -> Optional[FitnessClass]:
        """Gets a single fitness class by its ID."""
        all_class_types = with_polymorphic(FitnessClass, "*")
        return (
            session.query(all_class_types)
            .filter(FitnessClass.id == class_id)
            .first()
        )

    def get_all_fitness_classes(self, session: Session):
        """Gets a list of all fitness classes with pagination."""
        all_class_types = with_polymorphic(FitnessClass, "*")
        fitness_classes = session.query(all_class_types).all()
        return fitness_classes

    def get_fitness_class_with_lock(self, session: Session, class_id: int) -> Optional[FitnessClass]:
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
