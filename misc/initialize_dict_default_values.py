"""Demo of initializing dictionaries with default values."""

from typing import Any


def initialize_dict_values(
    keys: list[str],
    default_value: Any,
    dictionary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create or extend a dictionary by setting *keys* to *default_value*.

    Args:
        keys: List of keys to add.
        default_value: The value to assign to every key.
        dictionary: An existing dict to extend. If ``None``, a new dict is created.

    Returns:
        The updated (or newly created) dictionary.
    """
    base = dictionary if dictionary is not None else {}
    return {**base, **dict.fromkeys(keys, default_value)}


if __name__ == "__main__":
    keys = ["name", "age", "email"]
    result = initialize_dict_values(keys, "N/A")
    print(f"New dict: {result}")

    existing = {"role": "admin"}
    merged = initialize_dict_values(keys, 0, existing)
    print(f"Merged:   {merged}")
