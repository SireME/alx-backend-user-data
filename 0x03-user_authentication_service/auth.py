#!/usr/bin/env python3
"""
This module handles user suthentication
"""
from user import User


def _hash_password(password: str) -> bytes:
    """
    Method to hash password
    used from the User class
    """
    return User.set_password(User, password)
