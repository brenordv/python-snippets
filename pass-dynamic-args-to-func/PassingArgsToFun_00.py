#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PassingArgsToFun_00.py.py: Simple demo of how to pass arguments to functions.
Usual basic options.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


from base_sample_func import *



print("Just informing the mandatory argument...")
get_food(15)    

print("\r\n\r\nInforming all arguments by position...")
get_food(2, "Carrtos", False, False)

print("\r\n\r\nInforming the mandatory argument using it's name...")
get_food(quantity = 42)

print("\r\n\r\nInforming all arguments by name...")
get_food(quantity = 2, food = "Carrtos", express = False, is_awesome = False)

