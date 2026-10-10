"""Helpers for building SQL safely when a value can't be query parameter.

Prefer parameters: con.execute("... WHERE id = ?", [listing_id]).
Table names can't be parameters, so they are validated here, and text that
must go inside the SQL itself is escaped.
"""

import re

SAFE_IDENTIFIER_RE= re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")

def is_safe_identifier(name: str) -> str: 
    """Check if the given name is a safe SQL identifier and not malicious."""
    if not SAFE_IDENTIFIER_RE.match(name):
        raise ValueError(f"Unsafe SQL identifier: {name!r}")
    return name

def string_literal(value: str) -> str:
    """ Return 'value' as a quoted SQL string, escaping any single quotes inside it. """
    return "'" + value.replace("'", "''") + "'"