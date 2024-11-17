#!/usr/bin/env python3
"""Module: session_auth"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session based authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a session ID for a user ID

        :param user_id: The user ID
        :return: The session ID
        """
        if not user_id or not isinstance(user_id, str):
            return None
        from uuid import uuid4

        session = str(uuid4())
        self.user_id_by_session_id[session] = user_id
        return session

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Retrieves User ID based on Session ID
        :param session_id: The session ID
        :return: The User ID
        """
        if not session_id or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Retrieves the User instance based on a cookie value
        :param request: The request object
        :return: The User instance
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(session_id)

        from models.user import User
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        Remove session from in memory storage

        :param request:
        :return:
        """
        if not request:
            return None

        session = self.session_cookie(request)
        if not session:
            return False

        user_id = self.user_id_for_session_id(session)
        if not user_id:
            return False

        self.user_id_by_session_id.pop(session)
        return True
