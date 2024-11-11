#!/usr/bin/env python3
"""Module: filtered_logger"""
import re
import logging
from typing import List


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

    def __init__(self, fields: List):
        self.fields: List = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """Convert a LogRecord object to a redacted output"""
        original_message: str = super(RedactingFormatter, self).format(record)
        return filter_datum(
            self.fields, self.REDACTION, original_message, self.SEPARATOR
        )
