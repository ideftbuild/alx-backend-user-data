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
        """Verify presence of User record in the database
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

    def create_session(self, email: str) -> str:
        """Generate a UUID and store it in the database as
        the user's session_id.
        """
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=_generate_uuid())
            return user.session_id
        except NoResultFound:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """Retrieve a User record based on session_Id"""
        if not session_id:
            return None
        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        """Remove a User session from record in the database"""
        if not user_id:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass
