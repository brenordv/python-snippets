#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
print-sty.py: Demo of how to use sty package to print in colored.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


# Importing stuff...
from sty import fg, bg, ef, rs

# Testing Success/Warning/Error messages...
print(fg.red + 'ERROR Test!' + fg.rs)
print(fg.li_yellow + 'WARNING Test!' + fg.rs)
print(fg.green + 'SUCCESS Test!' + fg.rs)


# Other uses...
print(bg.blue + 'This has a powershell-blue background!' + bg.rs)
print(ef.italic + 'This is italic text' + rs.italic)

# Creating new colors...
fg.orange = ('rgb', (255, 150, 50))
print(fg.orange + 'Hey apple!' + fg.rs)
