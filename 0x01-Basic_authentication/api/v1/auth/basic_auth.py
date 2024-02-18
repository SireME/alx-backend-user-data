#!/usr/bin/env python3
"""Module for user authentication"""
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """
    This module implements basic authentication
    """
    def extract_base64_authorization_header(self, a: str) -> str:
        """
        method to return authorization header
        """
        authorization_header = a
        if authorization_header is None:
            return None

        if not isinstance(authorization_header, str):
            return None

        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(self, b: str) -> str:
        """
        decode b64 data if decodable
        """
        base64_authorization_header = b
        if b is None:
            return None
        if not isinstance(b, str):
            return None
        try:
            decodebyte = base64.b64decode(b)
            decodestr = decodebyte.decode('utf-8')
            return decodestr
        except Exception:
            return None
