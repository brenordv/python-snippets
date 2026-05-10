"""Two approaches to removing duplicate dicts from a list."""

from typing import Any


def remove_duplicates_basic(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove duplicates using a simple loop.

    Args:
        items: A list of dicts that may contain duplicates.

    Returns:
        A new list with unique items (preserving the last occurrence).
    """
    unique: list[dict[str, Any]] = []
    for i, item in enumerate(items):
        if item not in items[i + 1:]:
            unique.append(item)
    return unique


def remove_duplicates_comprehension(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Remove duplicates using a list comprehension.

    Args:
        items: A list of dicts that may contain duplicates.

    Returns:
        A new list with unique items (preserving last occurrence).
    """
    return [item for i, item in enumerate(items) if item not in items[i + 1:]]


if __name__ == "__main__":
    sample_data: list[dict[str, Any]] = [
        {"foo": 42, "bar": "bacon", "age": 100, "need_food": True},
        {"foo": 42, "bar": "bacon", "age": 100, "need_food": True},
        {"foo": 20, "bar": "bacon", "age": 50, "need_food": True},
    ]

    print("Method 1 -- basic loop:")
    for item in remove_duplicates_basic(sample_data):
        print(f"  {item}")

    print()

    print("Method 2 -- list comprehension:")
    for item in remove_duplicates_comprehension(sample_data):
        print(f"  {item}")
