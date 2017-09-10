#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mainscript.py: Main script for snippet demonstrating how to get the path for the
current script.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


import os
import mods.mymod

if __name__ == "__main__":
    main_path = os.getcwd()
    print("Main script path: %s" % main_path)
    
    mods.mymod.where_am_i()