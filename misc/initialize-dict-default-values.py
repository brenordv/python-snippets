#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
initialize-dict-default-values.py: Simple demo of how to initialize dictionaries with default values.
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

def initialize_dict_values(keys, default_value, dictionary=dict()):
    """Adds keys to the dictionary with a default value.
    If no dictionary is provided, will create a new one.

    :param keys: List of strings containing the dictionary keys
    :param default_value: default value to be associated with the keys
    :param dictionary: dictionary that will receive the keys
    :return: updated dictionary
    """

    return {**dictionary, **{ **dict.fromkeys(keys, default_value)}}
