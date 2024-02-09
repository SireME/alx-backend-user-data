#!/usr/bin/env python3
"""
Module to encrypt passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a randomly generated salt.

    Args:
        password: The password to be hashed.

    Returns:
        bytes: The salted, hashed password as a byte string.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
