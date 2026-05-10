"""Demo of checking whether user input is a number (int or float)."""

from __future__ import annotations


def is_number(value: str) -> bool:
    """Check whether a string can be interpreted as a number.

    Args:
        value: The string to test.

    Returns:
        True if the string represents a valid int or float.
    """
    try:
        float(value)
        return True
    except (ValueError, TypeError):
        return False


def should_exit(user_input: str, exit_flag: str = "exit") -> bool:
    """Check if the user input matches the exit flag.

    Args:
        user_input: The string entered by the user.
        exit_flag: The keyword that signals exit.

    Returns:
        True if the user wants to exit.
    """
    return user_input.lower().strip() == exit_flag


def main() -> None:
    """Interactive loop that checks if each input is a number."""
    user_input = ""

    print("(To exit, type 'exit' and press Enter.)")

    while not should_exit(user_input):
        user_input = input("Hello! Please, input a number: ")

        if not should_exit(user_input):
            if is_number(user_input):
                print(f"Great! A valid number! You chose: {user_input}")
            else:
                print(f"Sorry. I'm pretty sure that '{user_input}' is not a number.")

    print("\nOk. See you later.\nThanks for all the fish!")


if __name__ == "__main__":
    main()
