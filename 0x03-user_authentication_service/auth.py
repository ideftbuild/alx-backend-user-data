#!/usr/bin/env python3
"""Module: auth"""


def _hash_password(password: str) -> bytes:
    """Generate a bcrypt hash of the given password."""
    import bcrypt
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)
