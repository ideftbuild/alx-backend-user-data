#!/usr/bin/env python3
"""Module: basic_auth"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Authentication class"""

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """
        Extracts the Base64 part of the Authorization header.

        :param authorization_header: The Authorization header string.
        :return: The Base64 encoded part of the Authorization header,
        or None if invalid.
        """
        if not authorization_header:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith('Basic '):
            return None
        return authorization_header[6:]
