#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
relative_dates.py: Getting a new relative date.
"""
from datetime import datetime
from dateutil.relativedelta import relativedelta

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

#Base date
base_date = datetime(2018,1,31,10,11,12)

#Add 1 month
new_date = base_date + relativedelta(months=+1)

#Print base date.
print(base_date)

#Print new date.
print(new_date)