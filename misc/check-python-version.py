#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
check-python-version.py: Simple way to check your Python version during runtime.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

import sys

#Where to get versin number. 
print(sys.version)

print("Current Python Version: %s" % sys.version.split(" ")[0])


print(sys.version_info)

print("\r\nVersion detail:")
version_detail  = "Major: %s\r\n" % sys.version_info[0]
version_detail += "Minor: %s\r\n" % sys.version_info[1]
version_detail += "Micro: %s\r\n" % sys.version_info[2]
version_detail += "Release Level: %s\r\n" % sys.version_info[3]
version_detail += "Serial: %s\r\n" % sys.version_info[4]
print(version_detail)


#Checking vesion during runtime.
if sys.version_info[0] < 3:
    print("Sorry, i need Python 3+ to run.")
else:
    print("Great! You have Python 3! Let's do stuff!")
