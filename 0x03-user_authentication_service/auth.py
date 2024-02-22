#!/usr/bin/env python3
"""
This module handles user suthentication
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Method to hash password
    """
    gen = bcrypt.gensalt()
    encd = password.encode('utf-8')
    hpwd = bcrypt.hashpw(encd, gen)
    return hpwd
