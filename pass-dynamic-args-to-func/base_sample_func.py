#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
base_sample_func.py: Holder for the sample function.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


def get_food(quantity, food="Bacon", express = True, is_awesome = True):
    """get_food: Sample function."""
    express_msg = "I'm hungry, please hurry!\r\n" if express else ""
    is_awesome_msg = "This is awesome!" if is_awesome else "nah..."
    print("%sHere's %s portions of %s.\r\n%s" % (express_msg, quantity, food, is_awesome_msg))
