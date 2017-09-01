#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PassingArgsToFun_01.py.py: Simple demo of how to pass arguments to functions.
Using a wrapper function, but doing things the hard/not-so-smart way here.
Just for demonstration purposes, i'll would never create a function like
that in real life. ;)
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


from base_sample_func import *

#Now, let's create a wrapper function, with all arguments being optional...
def wrapper_func_hard(quantity = None, food = None, express = None, is_awesome = None):
    """
    wrapper_func_hard: Sample wrapper function. 
    """
    
    if quantity is None:
        quantity = 42
    
    if food is None and express is None and is_awesome is None:
        get_food(quantity = quantity)
        return
        
    if food is not None and express is None and is_awesome is None:
        get_food(quantity = quantity, food = food)
        return
        
    if food is not None and express is not None and is_awesome is None:
        get_food(quantity = quantity, food = food, express = express)
        return
        
    if food is not None and express is not None and is_awesome is not None:
        get_food(quantity = quantity, food = food, express = express, is_awesome = is_awesome)
        return
    
    print("something went wrong... :(")
    
    
print("\r\n\r\nCalling wrapper function 'hard way'...")

print("\r\nCase 1: No args...")
wrapper_func_hard()


print("\r\nCase 2: Only first arg...")
wrapper_func_hard(quantity = 12)

print("\r\nCase 3: Only first 2 args...")
wrapper_func_hard(quantity = 12, food="cheese")

print("\r\nCase 4: Only first 3 args...")
wrapper_func_hard(quantity = 12, food="cheese", express=True)

print("\r\nCase 5: All 4 args...")
wrapper_func_hard(quantity = 12, food="cheese", express=True, is_awesome=True)

print("\r\nCase 6: Skipping one arg and breaking things...")
wrapper_func_hard(quantity = 12, food="cheese", is_awesome=True)