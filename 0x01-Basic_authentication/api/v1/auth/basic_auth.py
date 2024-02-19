#!/usr/bin/env python3
"""Module for user authentication"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


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

    def extract_user_credentials(self, d: str) -> (str, str):
        """
        extract email and password from str
        """
        decoded_base64_authorization_header = d
        non_r = (None, None)
        if d is None or not isinstance(d, str):
            return non_r
        if ':' not in d:
            return non_r
        if d.count(':') > 1:
            em_pwd = d.split(':')
            email = em_pwd[0]
            pwd = ':'.join(em_pwd[1:])
            email_and_password = [email, pwd]
        else:
            email_and_password = d.split(':')
        return tuple(email_and_password)

    def user_object_from_credentials(self, em: str, pwd: str):
        """
        return user instance based on email and pwd
        Args:
            pwd: user password
            em: user password
        return:
            None or User object : TypeVar('User')
        """
        user_email, user_pwd = em, pwd
        if em is None or not isinstance(em, str):
            return None

        if pwd is None or not isinstance(pwd, str):
            return None

        # Search for the user in db based on email
        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        # no user found with password
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """extract current user from request Authorization
        header and validate with the database
        """
        # get the authorization header: "Authorization"
        # from request format:Basic jvhbhvjhk
        a_h: str = self.authorization_header(request)

        # extract authorization header format: jvhbhvjhk
        ext = self.extract_base64_authorization_header(a_h)

        # decode authorization header format username:pwd
        decode = self.decode_base64_authorization_header(ext)

        # have email and pwd as tuple format: (email, pwd)
        ep = self.extract_user_credentials(decode)

        # get userobject from email and password
        user = self.user_object_from_credentials(ep[0], ep[1])

        return user
