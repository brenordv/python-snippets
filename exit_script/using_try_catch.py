"""Demonstrate running cleanup code when a script exits using try/except/finally."""

from __future__ import annotations


def run_on_exit() -> None:
    """Cleanup function called in the finally block."""
    print("\nHe's dead, Jim!")


def main() -> None:
    """Show try/except/finally as a cleanup pattern."""
    try:
        print("Hey there! Starting!")
        user_input = input(
            "Input 'EX' to raise an error, or press Ctrl+C to cancel: "
        )

        if user_input.lower().strip() == "ex":
            raise RuntimeError("User-triggered error for demonstration.")

    except RuntimeError as exc:
        print(f"Caught an exception: {exc}")

    finally:
        run_on_exit()


if __name__ == "__main__":
    main()
