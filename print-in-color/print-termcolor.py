#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
print-termcolor.py: Demo of how to use termcolor to print using colors.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

# Importing things...
from termcolor import colored

# Testing printing using colors.
print(colored('Error Test!!!', 'red'))
print(colored('Warning Test!!!', 'yellow'))
print(colored('Success Test!!!', 'green'))
