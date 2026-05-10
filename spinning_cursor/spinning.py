"""Simple spinning cursor animation for terminal output."""

from __future__ import annotations

import itertools
import sys
import time

SPINNER_FRAMES = itertools.cycle(("\\", "|", "/", "-"))


def spinning_cursor_with_label(label_text: str) -> None:
    """Display a spinning cursor followed by a label on the current line.

    Args:
        label_text: Message to display next to the spinner.
    """
    frame = next(SPINNER_FRAMES)
    sys.stdout.write(f"\r[{frame}]\t{label_text}")
    sys.stdout.flush()


def main() -> None:
    """Demo the spinning cursor with a simple loop."""
    for i in range(25):
        spinning_cursor_with_label(label_text=f"Processing thing {i}...")
        time.sleep(0.15)
    print()  # Final newline


if __name__ == "__main__":
    main()
