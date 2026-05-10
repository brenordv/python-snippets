"""Demonstration of argparse usage with various argument types."""

from __future__ import annotations

import argparse
from sys import argv

__version__ = "1.0.0"


def get_parsed_cmd_line(
    test_cmd: list[str] | None = None,
) -> argparse.Namespace:
    """Parse command-line arguments and return the resulting namespace.

    Args:
        test_cmd: Optional list of arguments to parse instead of sys.argv.

    Returns:
        Parsed arguments as an argparse.Namespace object.
    """
    parser = argparse.ArgumentParser(description="Argparse demo application")

    # Required INT argument
    parser.add_argument(
        "-i", "--number",
        required=True,
        dest="arg_num",
        type=int,
        help="Required numeric argument.",
    )

    # Required STRING argument
    parser.add_argument(
        "-s", "--string",
        required=True,
        dest="arg_str",
        type=str,
        help="Required string argument.",
    )

    # Optional INT argument
    parser.add_argument(
        "-oi", "--optional-number",
        dest="arg_opt_num",
        type=int,
        help="Optional numeric argument.",
    )

    # Optional argument without explicit type (defaults to str)
    parser.add_argument(
        "-oi2", "--optional-number2",
        dest="arg_opt_num2",
        help="Optional argument without explicit type.",
    )

    # Optional STRING argument
    parser.add_argument(
        "-os", "--optional-string",
        dest="arg_opt_str",
        type=str,
        help="Optional string argument.",
    )

    # Optional STRING argument with explicit store action
    parser.add_argument(
        "-os2", "--optional-string2",
        dest="arg_opt_str2",
        action="store",
        type=str,
        help="Optional string argument with explicit store action.",
    )

    # Boolean flag: store_true (default False)
    parser.add_argument(
        "-t", "--true",
        dest="arg_true",
        action="store_true",
        default=False,
        help="Flag that is True when provided, False otherwise.",
    )

    # Boolean flag: store_false (default True)
    parser.add_argument(
        "-f", "--false",
        dest="arg_false",
        action="store_false",
        default=True,
        help="Flag that is False when provided, True otherwise.",
    )

    # Boolean flag: store_false with no default
    parser.add_argument(
        "-n", "--no-default",
        dest="arg_flag",
        action="store_false",
        help="Flag that is False when provided (no explicit default).",
    )

    # List argument (append action)
    parser.add_argument(
        "-l", "--list",
        dest="arg_list",
        default=[],
        action="append",
        help="Appends values to a list (repeatable).",
    )

    # List of ints (append action)
    parser.add_argument(
        "-li", "--list-int",
        dest="arg_list_int",
        type=int,
        action="append",
        help="Appends integer values to a list (repeatable).",
    )

    # Unused list argument (append action, no default)
    parser.add_argument(
        "-lu", "--list-unused",
        dest="arg_list_unused",
        action="append",
        help="List argument with no default value.",
    )

    # Constant list flags (append_const action)
    parser.add_argument(
        "-lc1", "--list-const1",
        dest="arg_list_const",
        action="append_const",
        const="Flag 1",
        help="Appends constant 'Flag 1' to a list.",
    )

    parser.add_argument(
        "-lc2", "--list-const2",
        dest="arg_list_const",
        action="append_const",
        const="Flag 2",
        help="Appends constant 'Flag 2' to a list.",
    )

    # Version action
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Print the current version and exit.",
    )

    return parser.parse_args(args=test_cmd)


def main(test_cmd: list[str] | None = None) -> None:
    """Parse arguments and print each one with its type.

    Args:
        test_cmd: Optional list of arguments for testing purposes.
    """
    parsed_args = get_parsed_cmd_line(test_cmd=test_cmd)

    for key, value in vars(parsed_args).items():
        print(f"{key} => {value} (type: {type(value).__name__})")


if __name__ == "__main__":
    if len(argv) == 1:
        # No CLI args provided -- use a built-in example for demonstration.
        test_mode = "full"

        if test_mode == "full":
            test_cmdline: list[str] | None = [
                "-i", "42",
                "-s", "bacon is awesome!",
                "-oi", "21",
                "-oi2", "22",
                "-os", "juice",
                "-os2", "something else",
                "-t",
                "-f",
                "-n",
                "-l", "software",
                "-l", "hardware",
                "-l", "tupperware",
                "-li", "1",
                "-li", "3",
                "-li", "5",
                "-li", "7",
                "-lc1",
                "-lc2",
            ]
        elif test_mode == "version":
            test_cmdline = ["-v"]
        else:
            # Only required arguments
            test_cmdline = [
                "-i", "42",
                "-s", "bacon is awesome!",
            ]
    else:
        test_cmdline = None

    main(test_cmd=test_cmdline)
