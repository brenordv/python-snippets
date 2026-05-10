"""Split a string and strip whitespace -- the list-comprehension approach."""


def split_and_strip(text: str, sep: str = ",") -> list[str]:
    """Split *text* on *sep* and strip whitespace from each part.

    Args:
        text: The string to split.
        sep: The separator to split on.

    Returns:
        A list of trimmed strings.
    """
    return [part.strip() for part in text.split(sep)]


if __name__ == "__main__":
    foods = "bacon, meat, pork chop, landjaeger, hamburger"

    print(f"Before: {foods.split(',')}")
    print(f"After:  {split_and_strip(foods)}")
