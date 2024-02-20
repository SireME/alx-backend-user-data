#!/usr/bin/env python3
"""Module for user authentication"""

from flask import request
from models.user import User
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """Handles user authentication using session"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create session id
        Args:
            user_id: uuid id enerated to act as session id
        Return:
              session id
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        user_key = uuid.uuid4().__str__()
        cls = SessionAuth
        cls.user_id_by_session_id[user_key] = user_id
        return user_key
