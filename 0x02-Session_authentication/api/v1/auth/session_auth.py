#!/usr/bin/env python3
"""Module for user authentication"""

from flask import request
from models.user import User
from typing import List, TypeVar
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Handles user authentication using session"""
    pass
