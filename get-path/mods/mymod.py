#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
mymod.py: auxiliary file for demo.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

import os

def where_am_i():
    my_path = os.path.dirname(os.path.realpath(__file__))
    print("My Mod path is: %s" % my_path)