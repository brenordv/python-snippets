#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""argparse_demo.py: Simple demo of how to use argparse."""

__author__ = "Breno RdV"
__copyright__ = "Breno RdV @ raccoon.ninja"
__contact__ = "http://raccoon.ninja"
__license__ = "MIT"
__version__ = "01.000"
__maintainer__ = "Breno RdV"
__status__ = "Demonstration"

import argparse as args
from sys import argv


def get_parsed_cmd_line(test_cmd=None):
    """
    Processes the commandline arguments.
    :param test_cmd: Custom arguments.
    :return: parsed arguments.
    """

    # Instanciating commandline argument parser
    parser = args.ArgumentParser("Analyzing commandline...")

    # Adding arguments.
    # Adding required INT argument.
    parser.add_argument("-i", "--number",
                        required=True,
                        dest="arg_num",
                        type=int,
                        help="This is a required numeric argument.")

    # Adding required STRING argument.
    parser.add_argument("-s", "--string",
                        required=True,
                        dest="arg_str",
                        type=str,
                        help="This is a required string argument.")

    # Adding optional INT argument.
    parser.add_argument("-oi", "--optional-number",
                        required=False,
                        dest="arg_opt_num",
                        type=int,
                        help="This is an optional numeric argument.")

    # Adding optional INT argument without explicit type defined.
    parser.add_argument("-oi2", "--optional-number2",
                        required=False,
                        dest="arg_opt_num2",
                        help="This is an optional numeric argument without a type defined.")

    # Adding optional STRING argument.
    parser.add_argument("-os", "--optional-string",
                        required=False,
                        dest="arg_opt_str",
                        type=str,
                        help="This is an optional string argument.")

    # Adding optional STRING argument with explicit store action defined.
    parser.add_argument("-os2", "--optional-string2",
                        required=False,
                        dest="arg_opt_str2",
                        action="store",
                        type=str,
                        help="This is an optional string argument with explicit store action defined.")

    # Adding boolean flag argument.
    parser.add_argument("-t", "--true",
                        required=False,
                        dest="arg_true",
                        action="store_true",
                        default=False,
                        help="This is a flag argument. If informed, will be set to true, otherwise, will be false.")

    # Adding another boolean flag argument.
    parser.add_argument("-f", "--false",
                        required=False,
                        dest="arg_false",
                        action="store_false",
                        default=True,
                        help="This is a flag argument. If informed, will be set to false, otherwise, will be true.")

    # Adding yet another boolean flag argument.
    parser.add_argument("-n", "--no-default",
                        required=False,
                        dest="arg_flag",
                        action="store_false",
                        help="This is a flag argument. If informed, will be set to false. "
                             "No default configured for this.")

    # Adding a list argument.
    parser.add_argument("-l", "--list",
                        required=False,
                        dest="arg_list",
                        default=[],
                        action="append",
                        help="This is an optional list argument with default value defined.")

    # Adding a list argument that only accepts numbers, but there's no default value.
    parser.add_argument("-li", "--list-int",
                        required=False,
                        dest="arg_list_int",
                        type=int,
                        action="append",
                        help="This is an optional list of numbers argument with no default value defined.")

    # Adding yet another list argument without default value.
    parser.add_argument("-lu", "--list-unsed",
                        required=False,
                        dest="arg_list_unsused",
                        action="append",
                        help="This is an optional list argument with no default value defined.")

    # Adding flag that appends a constant to a list.
    parser.add_argument("-lc1", "--list-const1",
                        required=False,
                        dest="arg_list_const",
                        action="append_const",
                        const="Flag 1",
                        help="This is a flag that adds a constant value to a list.")

    # Adding flag that appends a constant to a list.
    parser.add_argument("-lc2", "--list-const2",
                        required=False,
                        dest="arg_list_const",
                        action="append_const",
                        const="Flag 2",
                        help="This is a flag that adds another constant value to a list.")

    # Adding an argument that prints the current version.
    parser.add_argument("-v", "--version",
                        action="version",
                        version="{} | ver {}".format(__file__, __version__),
                        help="Argument that prints the current version of your application.")

    if test_cmd:
        return parser.parse_args(args=test_cmd)
    else:
        return parser.parse_args(args=test_cmd)


def main(test_cmd=None):
    """
    Main function
    :param test_cmd: If informed, will consider this has the commandline arguments instead of the ones informed via
    the prompt.
    :return: None
    """
    processed_args = get_parsed_cmd_line(test_cmd=test_cmd)

    for key, value in processed_args.__dict__.items():
        print("{} => {} (type: {})".format(key, value, type(value)))


if __name__ == '__main__':
    if len(argv) == 1:
        # Set this to something other than full to change it from full to only required.
        # If set to version, will just print the current version.
        test_mode = "full"

        if test_mode == "full":
            # Full command line example.
            test_cmdline = [
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
                "-lc2"
            ]

        elif test_mode == "version":
            test_cmdline = ["-v"]

        else:
            # Only required.
            test_cmdline = [
                "-i", "42",
                "-s", "bacon is awesome!"
            ]
    else:
        test_cmdline = None

    main(test_cmd=test_cmdline)
