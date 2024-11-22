#!/usr/bin/env python3
"""Module: auth"""
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Generate a bcrypt hash of the given password."""
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)


def _generate_uuid() -> str:
    """Generate a new UUID4 string."""
    from uuid import uuid4
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Adds a new User record to the database."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            return self._db.add_user(
                email=email, hashed_password=str(_hash_password(password))
            )

    def valid_login(self, email: str, password: str) -> bool:
        """Check if user is registered
        :return: True if the password is valid, False otherwise
        """
        from bcrypt import checkpw
        from ast import literal_eval

        try:
            user = self._db.find_user_by(email=email)
            return checkpw(
                password.encode('utf-8'), literal_eval(user.hashed_password)
            )
        except NoResultFound:
            return False
