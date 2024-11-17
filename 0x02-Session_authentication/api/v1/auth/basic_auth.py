#!/usr/bin/env python3
"""Module: basic_auth"""
import base64

from api.v1.auth.auth import Auth
from typing import TypeVar


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
        except (Error, UnicodeDecodeError):
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
        partition = decoded_base64_authorization_header.partition(':')
        return partition[0], partition[2]

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str
    ) -> TypeVar('User'):
        """
        Retrieves User instance based on email and password

        :param user_email: The user email
        :param user_pwd: The user password
        :return: The instance
        """
        from models.user import User

        def validate(attr):
            return attr and isinstance(attr, str)
        if not validate(user_email) or not validate(user_pwd):
            return None
        return next(
            (user for user in User.search({'email': user_email})
             if user.is_valid_password(user_pwd)), None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the User instance for a request
        :param request: The request object
        :return: The user instance
        """
        auth_header = self.extract_base64_authorization_header(
            request.headers.get('Authorization'))
        data = self.decode_base64_authorization_header(auth_header)
        user_credentials = self.extract_user_credentials(data)
        return self.user_object_from_credentials(
            user_credentials[0], user_credentials[1])
