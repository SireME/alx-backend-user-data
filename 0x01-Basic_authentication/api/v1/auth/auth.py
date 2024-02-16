#!/usr/bin/env python3
"""Module for user authentication"""

from flask import request
from models.user import User
from typing import List, TypeVar


class Auth:
    """Handles user authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for a given path"""
        return False

    def authorization_header(self, request=None) -> str:
        """Extracts the authorization header from the request"""
        pass

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user based on the request"""
        return None
