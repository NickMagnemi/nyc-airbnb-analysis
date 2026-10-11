"""Helpers for building SQL safely when a value can't be a query parameter.

Rule of thumb, in order of preference:
1. Values (numbers, text in a WHERE clause): use parameters,
   connection.execute("... WHERE id = ?", [listing_id]). Never format them in.
2. Names YOU choose (tables duckpipe creates): validate_table_name, a strict allowlist.
3. Names the DATA chooses (columns in someone's CSV, which may contain spaces or
   capitals): quote_identifier, which escapes instead of rejecting.
4. Text that must sit inside SQL itself (file paths, regexes): string_literal.

C# equivalent: EF Core does all of this for you behind LINQ. Here you are the
ORM, so these four functions are your whole defence against SQL injection.

You wrote versions of validate_table_name and string_literal in the first
project, so port them over and add the two new functions.
"""

import re
from collections.abc import Mapping

from duckpipe.errors import UnsafeSqlError  # noqa: F401 - for your checks

TABLE_NAME_PATTERN = re.compile(r"[a-z_][a-z0-9_]*")


def validate_table_name(name: str) -> str:
    """Return `name` if it's a plain lowercase SQL name, otherwise raise UnsafeSqlError.

    Example: "raw_listings" passes; "Listings", "x; DROP TABLE y" and "" fail.
    """
    # TODO: use TABLE_NAME_PATTERN.fullmatch(name). Raise UnsafeSqlError with a
    #       message that includes the bad name (use !r so spaces are visible).
    raise NotImplementedError


def quote_identifier(name: str) -> str:
    """Return `name` as a double-quoted SQL identifier, escaping any quotes inside it.

    Examples:
        Neighbourhood Group  becomes  "Neighbourhood Group"
        a"b                  becomes  "a""b"   (the inner quote is doubled)
    Use this for column names that come from data files, which you don't control.
    """
    # TODO: wrap in double quotes and double any " already inside the name.
    #       Reject an empty name with UnsafeSqlError.
    raise NotImplementedError


def string_literal(value: str) -> str:
    """Return `value` as a single-quoted SQL string, escaping single quotes inside it.

    Example: it's  ->  'it''s'
    """
    # TODO: same idea as quote_identifier, with ' instead of ".
    raise NotImplementedError


def render_options(options: Mapping[str, object]) -> str:
    """Render reader options as SQL keyword arguments.

    Example: {"all_varchar": True, "delim": ","}  ->  all_varchar = true, delim = ','

    Keys must pass validate_table_name (option names are always plain).
    Values: bool -> true/false, int/float -> the number, str -> string_literal,
    list/tuple of str -> ['a', 'b']. Anything else raises UnsafeSqlError.
    Returns "" for an empty mapping.
    """
    # TODO: build one "key = value" string per option, then ", ".join them.
    #       Check bool BEFORE int: in Python, True is also an int.
    #       A small private helper, _render_value(value) -> str, keeps this short.
    raise NotImplementedError
