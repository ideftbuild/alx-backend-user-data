#!/usr/bin/env python3
"""Module: auth

This module implements the Auth class, which is used to authenticate
each request.
"""
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
        if not request:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        The current authenticated user
        """
        return None
