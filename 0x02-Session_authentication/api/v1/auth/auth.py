#!/usr/bin/env python3
"""Module for user authentication"""

from flask import request
from models.user import User
from typing import List, TypeVar
import os


class Auth:
    """Handles user authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks if authentication is required for a given path"""
        if path is None or excluded_paths is None:
            return True
        if len(excluded_paths) == 0:
            return True
        # Check if any excluded path matches the given path
        for excluded_path in excluded_paths:
            ep = excluded_path  # shorten name for pep8
            if ep.endswith('*') and path.startswith(ep.rstrip('*')):
                return False

            if path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Extracts the authorization header from the request"""
        #  If request is None, returns None
        # If request doesn’t contain the header key
        # Authorization, returns None
        if not request or not request.headers.get("Authorization"):
            return None

        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieves the current user based on the request"""
        return None

    def session_cookie(self, request=None):
        """
        Return a cookie value from a request
        """
        if request is None:
            return None
        session_name = os.getenv('SESSION_NAME')
        return request.cookies.get(session_name)
