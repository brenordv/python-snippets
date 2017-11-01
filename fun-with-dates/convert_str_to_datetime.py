#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
convert_str_to_datetime.py: Few demonstrations of how to convert string to datetime.
"""
from datetime import datetime
from dateutil.parser import parse

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

#Defining format...
datetime_in_string = "31/12/2000 - 23:59:59"

#Setting the date in a string var...
datetime_format = "%d/%m/%Y - %H:%M:%S"

#Converting string to datetime. Method 1
result = datetime.strptime(datetime_in_string, datetime_format)
print(result)

#Converting string to datetime. Method 2
result2 = parse(datetime_in_string)
print(result2)