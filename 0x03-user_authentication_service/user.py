#!/usr/bin/env python3
"""User model"""

from typing import Optional
from sqlalchemy import Column, Integer, String
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """User class"""
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    email: str = Column(String(250), nullable=False)
    hashed_password: str = Column(String(250), nullable=False)
    session_id: Optional[str] = Column(String(250), nullable=True)
    reset_token: Optional[str] = Column(String(250), nullable=True)

    def __repr__(self) -> str:
        """Returns a string representation of the User object"""
        return f"User: id={self.id}"

    @staticmethod
    def authenticate(email: str, password: str) -> Optional['User']:
        """
        Authenticates a user by matching the email and hashed password.
        Returns the User object if authentication is successful, otherwise
        None.
        """
        # Logic for authenticating the user
        # Example implementation:
        user = User.query.filter_by(email=email, hashed_password=password).\
            first()
        return user

    def set_session_id(self, session_id: str) -> None:
        """Sets the session ID for the user"""
        self.session_id = session_id

    def reset_password(self, reset_token: str, new_password: str) -> None:
        """Resets the user's password using a reset token"""
        # Logic for resetting the password
        # Example implementation:
        if self.reset_token == reset_token:
            self.hashed_password = new_password
            self.reset_token = None
