#!/usr/bin/env python3
"""Module: encrypt_password"""


def hash_password(password: str) -> bytes:
    """Returns a salted, hashed password, which is a byte string."""
    import bcrypt

    password = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password, salt)
