#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
get_uptime.py: Simple demo of how to get delta from two dates in a format like: 10 days, 12:57:40.332768
The output format is: N days, h:m:s.ms
"""
from datetime import datetime

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

#Initial (oldest) date.
date_init = datetime.strptime("5-8-2000 13:45:10.345", '%d-%m-%Y %H:%M:%S.%f')

#Final (newest) date.
date_final = datetime(year=2018, month=1, day=30)

#Datetime with delta between the two other dates.
date_diff = date_final - date_init

#Printing a in a friendly way.
print("Uptime: %s" % str(date_diff))
