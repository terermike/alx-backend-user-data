#!/usr/bin/env python3
"""DB module"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


VALID = ['id', 'email', 'hashed_password', 'session_id', 'reset_token']


class DB:
    """DB class"""

    def __init__(self):
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self):
        """Memoized session object"""
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adding user"""
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """returns the first row found in the users table"""
        if not kwargs or any(field not in VALID for field in kwargs):
            raise InvalidRequestError
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """method will use find_user_by to locate the user to update"""
        user = self.find_user_by(id=user_id)
        for i, j in kwargs.items():
            if i not in VALID:
                raise ValueError
            setattr(user, i, j)
        self._session.commit()
