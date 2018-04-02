#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
printer.py: Simple demo of how to print to console using colors.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


class printer():
    """Class to print using colors. """
    _colors_ = {
        **dict.fromkeys(("RED", "ERROR", "NO"), "\033[1;31m"),
        **dict.fromkeys(("GREEN", "OK", "YES"), "\033[0;32m"),
        **dict.fromkeys(("YELLOW", "WARN", "MAYBE"), "\033[0;93m"),
        "BLUE": "\033[1;34m",
        "CYAN": "\033[1;36m",
        "RESET": "\033[0;0m",
        "BOLD": "\033[;1m",
        "REVERSE": "\033[;7m"
    }


    def _get_color_(self, key):
        """Gets the corresponding color ANSI code... """
        try:
            return self._colors_[key]
        except:
            return self._colors_["RESET"]


    def print(self, msg , color="RESET"):
        """Main print function..."""

        # Get ANSI color code.
        color = self._get_color_(key=color)

        # Printing...
        print("{}{}{}".format(color, msg, self._colors_["RESET"]))


    def error(self, msg):
        """Print message in red..."""

        self.print(msg=msg, color="RED")


    def success(self, msg):
        """Print message in green..."""

        self.print(msg=msg, color="GREEN")


    def warning(self, msg):
        """Print message in yellow..."""

        self.print(msg=msg, color="YELLOW")

if __name__ == "__main__":
    p = printer()

    p.success("SUCCESS Test...")
    p.warning("WARN Test...")
    p.error("ERROR Test...")

