"""Simple way to check the Python version at runtime."""

import sys


def print_version_info() -> None:
    """Print detailed Python version information."""
    print(f"Python version: {sys.version}")
    print(f"Version string: {sys.version.split()[0]}")
    print(f"Version info:   {sys.version_info}")

    info = sys.version_info
    print(
        f"\nVersion detail:\n"
        f"  Major: {info.major}\n"
        f"  Minor: {info.minor}\n"
        f"  Micro: {info.micro}\n"
        f"  Release Level: {info.releaselevel}\n"
        f"  Serial: {info.serial}"
    )


def check_minimum_version(major: int = 3, minor: int = 10) -> bool:
    """Return True if the running Python meets the minimum version."""
    return sys.version_info >= (major, minor)


if __name__ == "__main__":
    print_version_info()
    print()

    if check_minimum_version(3, 10):
        print("Great! You have Python 3.10+. All good.")
    else:
        print("Sorry, Python 3.10+ is required.")
