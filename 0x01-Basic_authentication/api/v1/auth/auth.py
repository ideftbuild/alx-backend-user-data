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

        # Normalize path to consistently handle trailing slashes
        path = path.rstrip('/')

        for exc_path in excluded_paths:
            # Handle wildcard paths with ending '*'
            if (exc_path.endswith('*')
                    and path.startswith(exc_path.rstrip('*'))):
                return False
            # Handle exact path matches (ignoring trailing slashes)
            if path == exc_path.rstrip('/'):
                return False

        return True  # Authentication required if not matche found

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
