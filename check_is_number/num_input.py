"""Simple demo: prompt the user for a valid integer using str.isdigit()."""

from __future__ import annotations


def main() -> None:
    """Repeatedly prompt until the user enters a valid integer."""
    user_input = ""

    while not user_input.isdigit():
        user_input = input("Hello! Please, input a valid integer: ")

    print(f"Great work! A valid number! You chose: {user_input}.")


if __name__ == "__main__":
    main()
