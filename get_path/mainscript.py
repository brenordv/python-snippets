"""Demo of retrieving the current script's path and a module's path."""

import os
from pathlib import Path

from mods import mymod


def get_script_dir() -> Path:
    """Return the directory containing this script."""
    return Path(__file__).resolve().parent


if __name__ == "__main__":
    print(f"Main script directory: {get_script_dir()}")
    print(f"Working directory:     {os.getcwd()}")
    mymod.where_am_i()
