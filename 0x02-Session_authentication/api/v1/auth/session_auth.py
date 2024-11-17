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
