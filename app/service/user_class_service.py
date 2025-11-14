from typing import List

from sqlalchemy.orm import Session

from app.config import SessionLocal
from app.orm_models import UserClass
from app.repository.user_class_repo import UserClassRepository
from app.service.transactions import run_in_transaction


class UserClassService:
    def __init__(self, repository: UserClassRepository):
        self.repo = repository

    @run_in_transaction(SessionLocal)
    def get_enrollment_count(self, class_id: int, session: Session) -> int:
        """Gets the number of users signed up for a class."""
        return self.repo.get_enrollment_count_for_class(session, class_id=class_id)

    @run_in_transaction(SessionLocal)
    def sign_up_for_class(self, user_id: int, class_id: int, session: Session) -> UserClass:
        """
        Service to sign a user up for a class.
        Decorator handles all transaction logic.
        """
        # Check if user is already enrolled
        existing_reg = self.repo.get_user_class_by_id(session, user_id=user_id, class_id=class_id)
        if existing_reg:
            raise ValueError(f"User {user_id} is already enrolled in class {class_id}")

        new_user_class = self.repo.create_user_class(session, user_id=user_id, class_id=class_id)

        return new_user_class

    @run_in_transaction(SessionLocal)
    def drop_class(self, user_id: int, class_id: int, session: Session):
        """Service to drop a user from a class."""
        user_class = self.repo.get_user_class_by_id(session, user_id=user_id, class_id=class_id)
        if not user_class:
            raise ValueError(f"User {user_id} is not enrolled in class {class_id}")

        self.repo.delete_user_class(session, user_class)
        # Decorator will commit

    @run_in_transaction(SessionLocal)
    def set_payment_status(self, user_id: int, class_id: int, paid: bool, session: Session):
        """Service to update the payment status for an enrollment."""
        db_registration = self.repo.get_user_class_by_id(session, user_id=user_id, class_id=class_id)
        if not db_registration:
            raise ValueError(f"User {user_id} is not enrolled in class {class_id}")

        db_registration.paid = paid
        session.add(db_registration)
        # Decorator will commit
        return db_registration

    @run_in_transaction(SessionLocal)
    def get_enrollment_details(self, user_id: int, class_id: int, session: Session) -> UserClass:
        """Service to get a specific enrollment."""
        db_registration = self.repo.get_user_class_by_id(session, user_id=user_id, class_id=class_id)
        if not db_registration:
            raise ValueError(f"Enrollment not found for user {user_id} and class {class_id}")
        return db_registration

    @run_in_transaction(SessionLocal)
    def get_enrolled_class_ids(self, user_id: int, session: Session) -> List[int]:
        """Service to get all class IDs a user is enrolled in."""
        return self.repo.get_user_enrolled_class_ids(session, user_id=user_id)

    @run_in_transaction(SessionLocal)
    def get_unpaid_class_ids(self, user_id: int, session: Session) -> List[int]:
        """Service to get IDs of all unpaid classes for a user."""
        unpaid_enrollments = self.repo.get_unpaid_classes_by_user(session, user_id=user_id)
        return [reg.class_id for reg in unpaid_enrollments]

    @run_in_transaction(SessionLocal)
    def is_paid(self, session: Session, user_id, class_id):
        return self.repo.is_class_paid(session, user_id, class_id)

    @run_in_transaction(SessionLocal)
    def get_number_of_signups(self, class_id: int, session: Session) -> int:
        """Gets the number of users signed up for a class."""
        return self.repo.get_enrollment_count_for_class(session, class_id=class_id)

    @run_in_transaction(SessionLocal)
    def update_status(self, user_id: int, class_id: int, status: str, session: Session):
        self.repo.update_status(session, user_id, class_id, status)

    @run_in_transaction(SessionLocal)
    def get_status(self, user_id: int, class_id: int, session: Session):
        return self.repo.get_status(session, user_id, class_id)