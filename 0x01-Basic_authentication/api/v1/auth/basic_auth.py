#!/usr/bin/env python3
"""Module for user authentication"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    This module implements basic authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        method to return authorization header
        """
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ')[1]
