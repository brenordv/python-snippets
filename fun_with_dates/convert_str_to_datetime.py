"""Demonstrations of how to convert a string to a datetime object."""

from datetime import datetime

from dateutil.parser import parse


def convert_with_strptime(date_string: str, date_format: str) -> datetime:
    """Convert a string to datetime using strptime with an explicit format.

    Args:
        date_string: The date string to parse.
        date_format: The expected format (e.g., "%d/%m/%Y - %H:%M:%S").

    Returns:
        A datetime object.
    """
    return datetime.strptime(date_string, date_format)


def convert_with_dateutil(date_string: str) -> datetime:
    """Convert a string to datetime using dateutil's fuzzy parser.

    Args:
        date_string: The date string to parse.

    Returns:
        A datetime object.
    """
    return parse(date_string)


if __name__ == "__main__":
    datetime_in_string = "31/12/2000 - 23:59:59"
    datetime_format = "%d/%m/%Y - %H:%M:%S"

    # Method 1: explicit format
    result1 = convert_with_strptime(datetime_in_string, datetime_format)
    print(f"strptime result: {result1}")

    # Method 2: dateutil parser (auto-detects format)
    result2 = convert_with_dateutil(datetime_in_string)
    print(f"dateutil result: {result2}")
