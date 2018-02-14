#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""longway.py: Simple (slightly better) demo of how to split a string and remove any extra spaces."""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

#Variables...
foods = "bacon, meat, pork chop, landjaeger, hamburger"

#Step00: Just to show the problem...
print("old:\t{0}".format(foods.split(",")))


#Step 01: Split the string and removes the spaces.
food_arr = [food.strip() for food in foods.split(',')]


#Final Step: Printing result...
print("new:\t{0}".format(food_arr))
