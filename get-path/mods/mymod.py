import os

def where_am_i():
    my_path = os.path.dirname(os.path.realpath(__file__))
    print("My Mod path is: %s" % my_path)