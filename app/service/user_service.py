from typing import Optional

from sqlalchemy.orm import Session

from app.config import SessionLocal
from app.orm_models.user import User
from app.pydantic_models import UserCreate
from app.repository.user_repo import UserRepository
from app.service.transactions import run_in_transaction


class UserService:
    def __init__(self, repository: UserRepository):
        self.repo = repository

    @run_in_transaction(SessionLocal)
    def create_user(self, user: UserCreate, session: Session) -> User:
        """
        Service to create a new user.
        Handles hashing password and transaction.
        """
        db_user = self.repo.get_user_by_username(session, user.username)
        if db_user:
            raise ValueError(f"Username '{user.username}' already registered.")

        new_user = self.repo.create_user(session, user.model_dump())
        return new_user

    @run_in_transaction(SessionLocal)
    def validate_user(self, username: str, password: str, session: Session) -> Optional[User]:
        """
        Service to validate user credentials.
        """
        db_user = self.repo.get_user_by_username(session, username=username)
        if not db_user:
            return None # User not found
        if not password == db_user.password:
            return None # Invalid password
        return db_user
