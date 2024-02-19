#!/usr/bin/env python3
"""Module for user authentication"""

from flask import request
from models.user import User
from typing import List, TypeVar


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
            path_end = path.split('/')[-1]
            if ep[-1] == '*' and ep.split('/')[-1][:-1] in path_end:
                path = excluded_path

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
