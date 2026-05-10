"""Demonstrate running cleanup code when a script exits using atexit."""

from __future__ import annotations

import atexit


def run_on_exit() -> None:
    """Callback executed when the interpreter shuts down."""
    print("\nHe's dead, Jim!")


def main() -> None:
    """Register the exit handler and interact with the user."""
    atexit.register(run_on_exit)

    print("Hey there! Starting!")
    user_input = input(
        "Input 'EX' to raise an error, or press Ctrl+C to cancel: "
    )

    if user_input.lower().strip() == "ex":
        raise RuntimeError("User-triggered error for demonstration.")


if __name__ == "__main__":
    main()
