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

    def create_session(self, email: str) -> str:
        """
        return session id(uuid) from email
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                s_id = _generate_uuid()
                setattr(user, 'session_id', s_id)
                return s_id
        except Exception:
            pass

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        return User from session_id
        """
        try:
            user = self._db.find_user_by(session_id=session_id)
            if user:
                return user
        except Exception:
            pass
        return None

    def destroy_session(self, user_id) -> None:
        """
        method to destroy a session id/reset it to None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            if user:
                setattr(user, 'session_id', None)
        except Exception:
            pass
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        method to get password reset token
        from email
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                reset_token = _generate_uuid()
                setattr(user, 'reset_token', reset_token)
                return reset_token
        except NoResultFound:
            raise ValueError

        def update_password(reset_token: str, password: str) -> None:
            """
            hash and update password using reset token
            """
            try:
                rt = reset_token
                user = self._db.find_user_by(reset_token=rt)

                hashed_password = _hash_password(password)
                # replace password with new one and remove reset token
                self._db.update_user(user.id, hashed_password=hashed_password)
                self._db.update_user(user.id, reset_token=None)

            except NoResultFound:
                raise ValueError
