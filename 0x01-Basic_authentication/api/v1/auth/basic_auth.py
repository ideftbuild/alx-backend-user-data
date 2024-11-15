#!/usr/bin/env python3
"""Module: basic_auth"""
import base64

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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """
        Decode base64 sting to UTF8

        :param base64_authorization_header: The base64 string to decode
        :return: The decoded  value as UTF8 string
        """
        if not base64_authorization_header:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None
        from base64 import b64decode
        from binascii import Error
        try:
            return b64decode(base64_authorization_header).decode('utf-8')
        except Error:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extract user email and password from decoded base64 string
        :param decoded_base64_authorization_header: The decoded base64 string
        :return: user email and password as a tuple
        """
        if not decoded_base64_authorization_header:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        return tuple(decoded_base64_authorization_header.split(':'))
