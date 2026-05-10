"""Demonstration of importing all files from a directory as a package.

Related blog post:
http://raccoon.ninja/pt/dev-pt/python-importando-todos-os-arquivos-de-um-diretorio/

The ``mods`` directory has an ``__init__.py`` that makes it a package, so its
modules can be imported directly.  The ``otherfiles`` directory does *not* have
one, so imports from it would fail with the standard mechanism.
"""

from mods.food import get_food
from mods.math_utils import calc_sum
from mods.ping import ping

# Note: otherfiles/misc.py cannot be imported this way because
# the otherfiles directory does not contain an __init__.py file.


if __name__ == "__main__":
    print("From food.py")
    print(f"{get_food()}\n")

    print("From math_utils.py")
    print(f"{calc_sum(4, 2)}\n")

    print("From ping.py")
    print(f"{ping()}\n")
