#!/usr/bin/env python3
"""
This module handles user suthentication
"""
import uuid
from user import User
from db import DB
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Method to hash password
    used from the User class
    """
    return User.set_password(User, password)


def _generate_uuid() -> str:
    """
    This method generates a random uuid
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        This method registers a user to the application
        """
        try:
            u = self._db.find_user_by(email=email)
            if u:
                message = f'User {email} already exists'
                raise ValueError(message)
        except NoResultFound:
            hp = _hash_password(password)
            obj = self._db.add_user(email=email, hashed_password=hp)
            return obj

    def valid_login(self, email: str, password: str) -> bool:
        """
        method to check if login is valid
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                return user.check_password(password)
        except Exception:
            return False
        return False
