from itertools import dropwhile
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import session_user

from app.orm_models.user_class import UserClass


class UserClassRepository:

    def get_user_class_by_id(self, session: Session, user_id: int, class_id: int) -> Optional[UserClass]:
        """Gets a UserClass association object by its composite key."""
        return session.get(UserClass, {"userId": user_id, "classId": class_id})

    def get_user_enrolled_class_ids(self, session: Session, user_id: int) -> List[int]:
        """
        Gets a list of class IDs a user is enrolled in.
        Replicates getUserEnrolledClassIds.
        """
        statement = select(UserClass.classId).where(UserClass.userId == user_id)
        return list(session.scalars(statement).all())

    def get_enrollment_count_for_class(self, session: Session, class_id: int) -> int:
        """
        Counts how many users are enrolled in a specific class.
        Replicates countUserClassById.
        """
        statement = select(func.count(UserClass.classId)).where(
            UserClass.classId == class_id
        )
        count = session.scalar(statement)
        return count if count is not None else 0

    def get_unpaid_classes_by_user(self, session: Session, user_id: int) -> List[UserClass]:
        """
        Finds all unpaid class registrations for a specific user.
        Replicates findUnpaidClassesByUserId.
        """
        statement = select(UserClass).where(
            UserClass.userId == user_id,
            UserClass.paid == False
        )
        return list(session.scalars(statement).all())

    def create_user_class(self, session: Session, user_id: int, class_id: int, paid: bool = False) -> UserClass:
        """Creates a new UserClass association (enrolls a user in a class)."""
        db_registration = UserClass(
            userId=user_id,
            classId=class_id,
            paid=paid
        )
        session.add(db_registration)
        session.commit()
        session.refresh(db_registration)
        return db_registration

    def delete_user_class(self, session: Session, user_class):
        session.delete(user_class)
        session.flush()

    def is_class_paid(self, session, user_id, class_id) -> bool:
        statement = select(UserClass.paid).where(UserClass.userId == user_id, UserClass.classId == class_id)

        result = session.scalars(statement).first()
        return bool(result) if result is not None else False
