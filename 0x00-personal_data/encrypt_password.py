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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against its hashed version.

    Args:
        hashed_password: The hashed password to compare against.
        password: The password to check.

    Returns:
        bool: True if the password matches the hashed password,
          False otherwise.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
