#!/usr/bin/env python3
"""Module: filtered_logger"""
import re
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Returns the log message obfuscated"""
    # Create a regex pattern to match the fields and their values
    pattern: str = f'({("|").join(fields)})=(.*?)(?={separator}|$)'
    # Substitute the field values with the redaction string
    return re.sub(fr'{pattern}', f'\\1={redaction}', message)
