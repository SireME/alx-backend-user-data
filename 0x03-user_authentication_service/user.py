#!/usr/bin/env python3
"""
sqlalchemy user model for users database table
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import bcrypt

Base = declarative_base()


class User(Base):
    """
    This class defines a SQLAlchemy model
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def set_password(self, password: str):
        """
        Method to hash password
        """
        gen = bcrypt.gensalt()
        encd = password.encode('utf-8')
        hpwd = self.hashed_password
        hpwd = bcrypt.hashpw(encd, gen).decode('utf-8')

    def check_password(self, password: str):
        """
        Method to check password
        """
        encd = password.encode('utf-8')
        hs_pwd = self.hashed_password.encode('utf-8')
        return bcrypt.checkpw(encd, hs_pwd)
