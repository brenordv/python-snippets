"""Utility to compute and display formatted elapsed time."""

from __future__ import annotations

import sys
from random import randint
from time import sleep, time

DEFAULT_FORMAT = "{hours:0>2}:{minutes:0>2}:{seconds:05.2f}"


def elapsed_time(
    start: float,
    end: float | None = None,
    time_format: str = DEFAULT_FORMAT,
) -> str:
    """Return a formatted string representing elapsed time.

    Args:
        start: Start timestamp (from time.time()).
        end: End timestamp. If None, the current time is used.
        time_format: Format string with {hours}, {minutes}, {seconds} placeholders.

    Returns:
        Formatted elapsed-time string.
    """
    if end is None:
        end = time()

    hours, remainder = divmod(end - start, 3600)
    minutes, seconds = divmod(remainder, 60)
    return time_format.format(
        hours=int(hours),
        minutes=int(minutes),
        seconds=seconds,
    )


def main() -> None:
    """Simulate work with a random sleep and print the elapsed time."""
    t_start = time()
    sleep_time = randint(3, 8)

    sys.stdout.write(f"Sleeping for {sleep_time} seconds")
    for _ in range(sleep_time):
        sys.stdout.write(".")
        sys.stdout.flush()
        sleep(1)

    print(f"\nElapsed time: {elapsed_time(start=t_start)}")


if __name__ == "__main__":
    main()
