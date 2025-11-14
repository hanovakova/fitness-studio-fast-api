from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.orm_models import User


class UserRepository:

    def get_user(self, session: Session, user_id: int) -> Optional[User]:
        """Gets a single user by their ID."""
        return session.get(User, user_id)


    def get_user_by_username(self, session: Session, username: str) -> Optional[User]:
        """Gets a single user by their username."""
        statement = select(User).where(User.username == username)
        return session.scalars(statement).first()


    def get_user_by_username_and_password(self, session: Session, username: str, password: str) -> Optional[User]:
        """
        Finds a user by username and password.

        SECURITY WARNING: This replicates your Java method, but you MUST NOT
        store passwords in plain text. Use a hashing library like 'passlib'.
        """
        print("SECURITY WARNING: Do not use plain text password matching in production.")
        statement = select(User).where(
            User.username == username,
            User.password == password
        )
        return session.scalars(statement).first()


    def get_users(self, session: Session, skip: int = 0, limit: int = 100) -> List[User]:
        """Gets a list of all users with pagination."""
        statement = select(User).offset(skip).limit(limit)
        return list(session.scalars(statement).all())


    def create_user(self, session: Session, user_data: dict) -> User:
        """
        Creates a new user.
        'user_data' should be a dictionary.
    
        """
        db_user = User(**user_data)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user
