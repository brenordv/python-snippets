"""Demonstration of ANSI terminal color codes for foreground and background text."""

from __future__ import annotations

RESET = "\033[0m"

COLORS: list[tuple[str, int, int]] = [
    ("Black",         30,  40),
    ("Red",           31,  41),
    ("Green",         32,  42),
    ("Yellow",        33,  43),
    ("Blue",          34,  44),
    ("Magenta",       35,  45),
    ("Cyan",          36,  46),
    ("Light Gray",    37,  47),
    ("Dark Gray",     90, 100),
    ("Light Red",     91, 101),
    ("Light Green",   92, 102),
    ("Light Yellow",  93, 103),
    ("Light Blue",    94, 104),
    ("Light Magenta", 95, 105),
    ("Light Cyan",    96, 106),
    ("White",         97, 107),
]


def main() -> None:
    """Print each ANSI color with foreground and background samples."""
    for name, fg_code, bg_code in COLORS:
        print(
            f"{RESET}** {name} ({fg_code})\n"
            f"\033[1;{fg_code}mForeground text{RESET}\n"
            f"\033[1;{bg_code}mBackground text{RESET}"
        )


if __name__ == "__main__":
    main()
