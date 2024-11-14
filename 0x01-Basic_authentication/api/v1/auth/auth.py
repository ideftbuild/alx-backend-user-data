#!/usr/bin/env python3
"""Module: auth"""
from flask import request
from typing import TypeVar, List


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if the given path requires authentication
        by checking against a list of excluded paths.
        """
        if not path or not excluded_paths:
            return True
        path = path if path.endswith('/') else path + '/'
        return path not in excluded_paths

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
