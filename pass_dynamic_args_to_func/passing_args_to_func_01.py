"""Demo 1: Wrapper function -- the hard (verbose) way.

Shows why manually checking every combination of optional arguments is tedious
and error-prone.  See passing_args_to_func_02.py for the cleaner approach.
"""

from base_sample_func import get_food


def wrapper_func_hard(
    quantity: int | None = None,
    food: str | None = None,
    express: bool | None = None,
    is_awesome: bool | None = None,
) -> None:
    """Call get_food by explicitly checking each argument combination."""
    if quantity is None:
        quantity = 42

    if food is None and express is None and is_awesome is None:
        get_food(quantity=quantity)
        return

    if food is not None and express is None and is_awesome is None:
        get_food(quantity=quantity, food=food)
        return

    if food is not None and express is not None and is_awesome is None:
        get_food(quantity=quantity, food=food, express=express)
        return

    if food is not None and express is not None and is_awesome is not None:
        get_food(quantity=quantity, food=food, express=express, is_awesome=is_awesome)
        return

    print("something went wrong... :(")


print("\n\nCalling wrapper function 'hard way'...")

print("\nCase 1: No args...")
wrapper_func_hard()

print("\nCase 2: Only first arg...")
wrapper_func_hard(quantity=12)

print("\nCase 3: Only first 2 args...")
wrapper_func_hard(quantity=12, food="cheese")

print("\nCase 4: Only first 3 args...")
wrapper_func_hard(quantity=12, food="cheese", express=True)

print("\nCase 5: All 4 args...")
wrapper_func_hard(quantity=12, food="cheese", express=True, is_awesome=True)

print("\nCase 6: Skipping one arg and breaking things...")
wrapper_func_hard(quantity=12, food="cheese", is_awesome=True)
