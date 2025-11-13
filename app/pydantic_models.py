from datetime import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel, field_validator, EmailStr, model_validator


# --- User Schemas ---

class UserBase(BaseModel):
    """Base schema for User, used for common fields."""
    username: str
    email: EmailStr = None
    name: Optional[str] = None
    advertisement: bool = False
    avatarPath: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user. Requires a password."""
    password: str


class User(UserBase):
    """Schema for reading/returning user data."""
    id: int

    class Config:
        orm_mode = True  # Renamed to from_attributes in Pydantic v2


# --- FitnessClass Schemas ---

class FitnessClassBase(BaseModel):
    """Base schema for FitnessClass."""
    name: Optional[str] = None
    description: Optional[str] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    instructorName: Optional[str] = None
    price: Optional[float] = None
    capacity: Optional[int] = None
    imagePath: Optional[str] = None


class FitnessClassCreate(FitnessClassBase):
    """Schema for creating any new class."""
    # This will be set in the service/router
    class_type: str = "fitness"


class YogaClassCreate(FitnessClassCreate):
    """Schema for creating a Yoga class."""
    yogaLevel: Optional[str] = None
    class_type: str = "yoga"


class SpinningClassCreate(FitnessClassCreate):
    """Schema for creating a Spinning class."""
    bikeType: Optional[str] = None
    class_type: str = "spinning"


class FitnessClass(FitnessClassBase):
    """Schema for reading/returning class data."""
    id: int
    class_type: str

    class Config:
        orm_mode = True


# --- UserClass Schemas ---

class UserClassBase(BaseModel):
    """Base schema for the association."""
    userId: int
    classId: int
    paid: bool = False


class UserClassCreate(UserClassBase):
    """Schema for enrolling a user in a class."""
    pass


class UserClass(UserClassBase):
    """Schema for reading a user's enrollment."""

    # You could add relationships here if needed
    # user: User
    # fitness_class: FitnessClass

    class Config:
        orm_mode = True


class RegistrationForm(BaseModel):
    """
    Pydantic model for validating the registration form.
    Matches the pattern from your `users.py` example.
    """
    username: str
    password: str
    password2: str
    name: str
    email: EmailStr
    advertisement: bool = False

    @field_validator('username')
    @classmethod
    def username_length(cls, v: str) -> str:
        if not 2 <= len(v) <= 16:
            raise ValueError("Username must be between 2 and 16 characters")
        return v

    @field_validator('password')
    @classmethod
    def password_length(cls, v: str) -> str:
        if len(v) < 4:
            raise ValueError("Password is too short (min 4 characters)")
        return v

    @model_validator(mode='after')
    def passwords_match(self) -> 'RegistrationForm':
        if self.password != self.password2:
            raise ValueError("Passwords do not match")
        return self


class FitnessClassDTO(FitnessClass):
    pass

class PurchaseEvent(BaseModel):
    event_id: uuid.UUID
    user_id: int
    classes: List[FitnessClassDTO]
    total_sum: float
    timestamp: datetime
