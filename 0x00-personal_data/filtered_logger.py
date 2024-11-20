#!/usr/bin/env python3
"""Module: filtered_logger"""
import re
import logging
from typing import List, Tuple
from mysql.connector import connect
from mysql.connector.connection import MySQLConnection
# from mysql.connector.pooling import PooledMySQLConnection

PII_FIELDS = ('password', 'phone', 'email', 'ssn', 'name')


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns the log message obfuscated"""
    # Create a regex pattern to match the fields and their values
    pattern: str = f'({("|").join(fields)})=(.*?)(?={separator}|$)'
    # Substitute the field values with the redaction string
    return re.sub(fr'{pattern}', f'\\1={redaction}', message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: Tuple):
        self.fields: List = list(fields)
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Convert a LogRecord object to a redacted output"""
        original_message: str = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
        )


def get_logger() -> logging.Logger:
    """Create a logger object and a handler set to level INFO
    :return: logging.Logger object
    """
    logger = logging.getLogger("user_data")  # Create logger object
    logger.setLevel(logging.INFO)  # Set message processing level
    logger.propagate = False
    # Create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)  # set handler level
    ch.setFormatter(RedactingFormatter(PII_FIELDS))

    logger.addHandler(ch)
    return logger


def get_db() -> MySQLConnection:
    """Connect to a database and return the connection object"""
    from os import getenv
    username = getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db = getenv('PERSONAL_DATA_DB_NAME')

    return connect(
        host=host,
        username=username,
        password=password,
        database=db,
        collation='utf8mb4_general_ci'
    )


def main():
    """Obtain a database connection and retrieve all
    rows from the users table"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT * FROM users')
    logger = get_logger()
    for row in cursor:
        logger.info("; ".join(f'{c[0]}={c[1]}' for c in row.items())
                    + RedactingFormatter.SEPARATOR)


if __name__ == '__main__':
    main()
