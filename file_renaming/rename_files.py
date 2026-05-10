"""Batch-rename files matching a three-part naming pattern.

Renames files of the form 'Part1 - Part2 - Part3.ext' to 'Part1__Part2.ext'
(with spaces replaced by underscores) in the specified directory.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

PATTERN = re.compile(r".+ - .+ - .+\..+")


def rename_files(path: str | Path, *, dry_run: bool = True) -> None:
    """Rename files that match the three-part pattern.

    Files matching 'A - B - C.ext' are renamed to 'A__B.ext' with spaces
    replaced by underscores.

    Args:
        path: Directory containing the files to rename.
        dry_run: If True, only print what would be renamed without making changes.
    """
    directory = Path(path)

    for filename in os.listdir(directory):
        if not PATTERN.match(filename):
            continue

        parts = filename.split(" - ")
        if len(parts) < 3:
            print(f"Skipping '{filename}': does not have 3 parts.")
            continue

        # Extract extension from the last part
        extension = parts[-1].split(".", 1)[1]
        new_name = f"{parts[0]}__{parts[1]}.{extension}".replace(" ", "_")

        old_file = directory / filename
        new_file = directory / new_name

        if dry_run:
            print(f"Would rename: {old_file} -> {new_file}")
        else:
            old_file.rename(new_file)
            print(f"Renamed: {old_file} -> {new_file}")


def main() -> None:
    """Run the rename utility in dry-run mode with an example path."""
    rename_files(path="c:/path/to/files", dry_run=True)


if __name__ == "__main__":
    main()
