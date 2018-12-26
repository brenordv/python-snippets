# -*- coding: utf-8 -*-

"""
elapsed_time.py: Shows formatted elapsed time.
"""

__author__ = "Breno RdV"
__copyright__ = "Breno RdV @ raccoon.ninja"
__contact__ = "http://raccoon.ninja"
__license__ = "MIT"
__version__ = "01.000"
__maintainer__ = "Breno RdV"
__status__ = "Demonstration"


from time import time, sleep
from random import randint
from sys import stdout


def elapsed_time(start, end=None, time_format="{hours:0>2}:{minutes:0>2}:{seconds:05.3f}"):
    """
    Returns a string with formatted elapsed time.
    :param start: time with start reference.
    :param end: time with end reference. If None, will use current time.
    :param time_format: Format string. If ommited, will use default.
    :return: formatted string.
    """

    if end is None:
        end = time()

    hours, r = divmod(end - start, 3600)
    minutes, seconds = divmod(r, 60)
    return time_format.format(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )


if __name__ == '__main__':
    t_start = time()

    # Time that the script will sleep... Just to simulate a work being done.
    sleep_time = randint(10, 20)

    # Printing out the passage of time...
    stdout.write("Sleeping for {} seconds".format(sleep_time))
    for i in range(sleep_time):
        stdout.write(".")
        stdout.flush()
        sleep(1)

    # Getting elapsed time and printing it out.
    print("\nElapsed time: {}".format(elapsed_time(start=t_start)))
