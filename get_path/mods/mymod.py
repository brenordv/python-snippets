"""Auxiliary module that reports its own file-system location."""

from pathlib import Path


def where_am_i() -> None:
    """Print the directory where this module lives."""
    my_path = Path(__file__).resolve().parent
    print(f"mymod path: {my_path}")
