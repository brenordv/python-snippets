#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""ImportFromDir.py: Demonstration of how to import all files from a folder."""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

from mods.Food import *
from mods.Math import *
from mods.Ping import *

#Not possible to do this. Otherfiles folder dont have a __init__.py file.
#from otherfiles.Misc imort *


print("From Food.py")
print(get_food() + "\r\n")

print("From Math.py")
print(str(calc_sum(4, 2)) + "\r\n")

print("From Ping.py")
print(ping() + "\r\n")