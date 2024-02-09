#!/usr/bin/env python3
"""
This module handles personal data
"""

from typing import List
import re
import logging
from os import environ
import mysql.connector


SENSITIVE_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_data(fields: List[str], replacement: str,
                message: str, delimiter: str) -> str:
    """
    Replaces sensitive information in a message with a replacement value
    based on the list of fields to redact

    Args:
        fields: list of fields to redact
        replacement: the value to use for redaction
        message: the string message to filter
        delimiter: the delimiter to use between fields

    Returns:
        The filtered string message with redacted values
    """
    for field in fields:
        message = re.sub(f'{field}=.*?{delimiter}',
                         f'{field}={replacement}{delimiter}', message)
    return message


def setup_logger() -> logging.Logger:
    """
    Returns a Logger object for handling Personal Data

    Returns:
        A Logger object with INFO log level and CustomFormatter
        formatter for filtering PII fields
    """
    logger = logging.getLogger("personal_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(CustomFormatter(list(SENSITIVE_FIELDS)))
    logger.addHandler(stream_handler)

    return logger


def connect_database() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a MySQLConnection object for accessing Personal Data database

    Returns:
        A MySQLConnection object using connection details from
        environment variables
    """
    username = environ.get("PERSONAL_DB_USERNAME", "root")
    password = environ.get("PERSONAL_DB_PASSWORD", "")
    host = environ.get("PERSONAL_DB_HOST", "localhost")
    db_name = environ.get("PERSONAL_DB_NAME")

    connection = mysql.connector.connection
    connection = connection.MySQLConnection(user=username,
                                            password=password,
                                            host=host,
                                            database=db_name)
    return connection


def main():
    """
    Main function to retrieve user data from database and log to console
    """
    db_connection = connect_database()
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = setup_logger()

    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db_connection.close()


class CustomFormatter(logging.Formatter):
    """
    Custom Formatter class for filtering PII fields
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    DELIMITER = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor method for CustomFormatter class

        Args:
            fields: list of fields to redact in log messages
        """
        super(CustomFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Formats the specified log record as text.

        Filters values in incoming log records using filter_data.
        """
        s = self.fields
        r = self.REDACTION
        rc = record.getMessage()
        dl = self.DELIMITER
        record.msg = filter_data(s, r, rc, dl)
        return super(CustomFormatter, self).format(record)


if __name__ == '__main__':
    main()
