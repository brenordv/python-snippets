"""Extract lines matching a search term from a file and write them to another file.

Note: A Rust version of this tool exists at https://github.com/brenordv/rusted-toolbox
"""

from __future__ import annotations

from pathlib import Path


def extract_lines(
    input_path: str | Path,
    output_path: str | Path,
    search_term: str,
) -> int:
    """Read *input_path* line-by-line and write matching lines to *output_path*.

    Args:
        input_path: Path to the source file.
        output_path: Path to the destination file (created/overwritten).
        search_term: Substring to search for in each line.

    Returns:
        The number of matching lines found.
    """
    lines_found = 0

    with open(output_path, "w", encoding="utf-8") as out_f, \
         open(input_path, "r", encoding="utf-8") as in_f:
        for line_num, line in enumerate(in_f, start=1):
            if search_term in line:
                lines_found += 1
                print(f"Found '{search_term}' in line {line_num}...")
                out_f.write(line)

    print(f"Found {lines_found} matching lines.")
    return lines_found


def main() -> None:
    """Run the extraction with example parameters."""
    in_file = "big_logfile.txt"
    out_file = "file_with_extracted_lines.txt"
    search_for = "ERROR"

    extract_lines(in_file, out_file, search_for)


if __name__ == "__main__":
    main()
