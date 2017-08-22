#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""NumInput2.py: Simple demo of how to check if a user input is a number."""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

user_input = "not a number"

while(not user_input.isdigit()):
    user_input = input("Hello! Please, input a (valid) integer: ")
    
print("Great work! A valid number! :D You chose: %s." % user_input)