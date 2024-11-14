#!/usr/bin/env python3
"""Module: auth"""
from flask import request
from typing import TypeVar, List


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if a user require authentication or not
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Retrieves information from the authorization header
        """
        return request

    def current_user(self, request=None) -> TypeVar('User'):
        """
        The current authenticated user
        """
        return request
