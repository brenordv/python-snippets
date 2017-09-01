#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
PassingArgsToFun_02.py.py: Simple demo of how to pass arguments to functions.
Using a new wrapper function that will handle arguments with a dictionary.
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
#But now we'll use a dictionary to handle the arguments.
def wrapper_func_easy(quantity = None, food = None, express = None, is_awesome = None):
    """
    wrapper_func_easy: Sample wrapper function. 
    """
    
    dict_args = {}
    
    dict_args['quantity'] = 42 if quantity is None else quantity
    
    if food is not None:
        dict_args['food'] = food
        
    if express is not None:
        dict_args['express'] = express

    if is_awesome is not None:
        dict_args['is_awesome'] = is_awesome
  
    get_food(**dict_args)

    
    
print("\r\n\r\nCalling wrapper function 'easy way'...")

print("\r\nCase 1: No args...")
wrapper_func_easy()

print("\r\nCase 2: Only first arg...")
wrapper_func_easy(quantity = 12)

print("\r\nCase 3: Only first 2 args...")
wrapper_func_easy(quantity = 12, food="cheese")

print("\r\nCase 4: Only first 3 args...")
wrapper_func_easy(quantity = 12, food="cheese", express=True)

print("\r\nCase 5: All 4 args...")
wrapper_func_easy(quantity = 12, food="cheese", express=True, is_awesome=True)

print("\r\nCase 6: Skipping one arg and NOT breaking things...")
wrapper_func_easy(quantity = 12, food="cheese", is_awesome=True)