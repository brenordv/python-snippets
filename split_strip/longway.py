"""Split a string and strip whitespace -- the explicit loop approach."""


def split_and_strip_loop(text: str, sep: str = ",") -> list[str]:
    """Split *text* on *sep* and strip whitespace from each part using a loop.

    Args:
        text: The string to split.
        sep: The separator to split on.

    Returns:
        A list of trimmed strings.
    """
    result: list[str] = []
    for part in text.split(sep):
        result.append(part.strip())
    return result


if __name__ == "__main__":
    foods = "bacon, meat, pork chop, landjaeger, hamburger"

    print(f"Before: {foods.split(',')}")
    print(f"After:  {split_and_strip_loop(foods)}")
