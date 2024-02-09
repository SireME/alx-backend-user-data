#!/usr/bin/env python3
"""
Filtered Logger Module
"""
import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    Obfuscate specified fields in the log message.
    """
    # Construct the regular expression pattern to match field values to obfuscate
    regex_pattern = '|'.join(f'({field}=)([^{separator}]+)' for field in fields)
    # Use regular expression substitution to replace field values with redaction
    obfuscated_message = re.sub(regex_pattern, lambda match: match.group(1) + redaction if match.group(1) else '', message)
    return obfuscated_message

 