# -*- coding: utf-8 -*-

"""serialize_datetime.py: Demo of how to serialize a datetime object."""

__author__      = "Breno RdV"
__copyright__   = "Breno RdV @ raccoon.ninja"
__contact__     = "http://raccoon.ninja"
__license__     = "MIT"
__version__     = "01.000"
__maintainer__  = "Breno RdV"
__status__      = "Demonstration"


from datetime import datetime
import json


def dt_parser(dt):
    """
    Parses (converts to string) a datetime object.
    :param dt: objeect to be converted.
    :return: dt object converted to string.
    """
    if isinstance(dt, datetime):
        return dt.isoformat()


if __name__ == '__main__':
    # Define the variable to be converted.
    foo = {"dt": datetime.now()}

    # 'Dumps' the dicionary to a string variable.
    bar = json.dumps(foo,
                     default=dt_parser)  # Informing our datetime converter.

    # Showing off the result.
    print(f"[{type(bar)}] {bar}")
