#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
UsingTryCath.py: How to run code at the end of a script's execution, using
try/catch/finally.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

def run_on_exit():
    print("\r\nHe's dead, Jim!")
    
    
if __name__ == "__main__":
    try:
        print("Hey there! Starting!")
        inp = input("Input EX to raise an error or just cancel this script (CTRL+C should work)...")
        
        if inp.lower().strip() == "ex":
            raise Exception
        
    except Exception:
        print("This used to work... EXCEPT this instance... ;-)")
        
    finally:
        run_on_exit()