#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
extract_lines.py: Demo of how to extract lines from a file.

Note: I created a tool in Rust that does the same thing: https://github.com/brenordv/rusted-toolbox
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

in_file = "big_logfile.txt" # Big file containing all the lines.
out_file = "file_with_extractedlines.txt" # File created with all the extracted lines.

search_for = "ERROR" # What to search in the log lines...
line_num = 0 # Line number
lines_found = 0 # Quantity of lines found...

with open(out_file, 'w') as out_f:
    with open(in_file, "r") as in_f:
        for line in in_f:
            line_num += 1
            if search_for in line:
                lines_found += 1
                print("Found '{}' in line {}...".format(search_for, line_num))
                out_f.write(line)

        print("Found {} lines...".format(lines_found))
