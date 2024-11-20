#!/usr/bin/env python3
"""Module: encrypt_password"""
from functools import wraps

import bcrypt


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string."""

    password = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password, salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates whether the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
