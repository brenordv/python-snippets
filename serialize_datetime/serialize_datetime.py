"""Demonstrate how to serialize datetime objects to JSON."""

from __future__ import annotations

import json
from datetime import datetime
from typing import Any


def datetime_serializer(obj: Any) -> str:
    """Convert datetime objects to ISO 8601 strings for JSON serialization.

    Args:
        obj: The object to serialize.

    Returns:
        ISO 8601 string representation if *obj* is a datetime.

    Raises:
        TypeError: If *obj* is not a datetime instance.
    """
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def main() -> None:
    """Serialize a dict containing a datetime and print the JSON string."""
    data: dict[str, Any] = {"dt": datetime.now()}
    result = json.dumps(data, default=datetime_serializer)
    print(f"[{type(result).__name__}] {result}")


if __name__ == "__main__":
    main()
