#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
spinning.py: Simple demo of a spinning cursor...
"""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.001"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"

import sys



CURSOR_POSITIONS = ('\\', '|', '/', '-')
CURRENT_CURSOR_POS = 0

def _get_next_cursor_():
    """Returns the next cursor position."""
    global CURRENT_CURSOR_POS
    try:
        CURRENT_CURSOR_POS += 1
        return CURSOR_POSITIONS[CURRENT_CURSOR_POS]
    except:
        CURRENT_CURSOR_POS = 0
        return CURSOR_POSITIONS[CURRENT_CURSOR_POS]


# Spinning cursor
def spinning_cursor_with_label(label_text):
    """Shows the spinning cursor with a message."""
    sys.stdout.write('\r[{}]\t{}'.format(_get_next_cursor_(), label_text))
    sys.stdout.flush()

if __name__ == "__main__":
    """Simple demo of a spinning cursor."""
    for i in range(25):
        spinning_cursor_with_label(label_text="Processing thing {}...".format(i))

