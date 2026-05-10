"""Demo 2: Wrapper function -- the easy way using **kwargs.

Builds a dict of only the non-None arguments and unpacks it into the target
function.  Compare with passing_args_to_func_01.py to see the improvement.
"""

from base_sample_func import get_food


def wrapper_func_easy(
    quantity: int | None = None,
    food: str | None = None,
    express: bool | None = None,
    is_awesome: bool | None = None,
) -> None:
    """Call get_food by collecting non-None arguments into a dict."""
    kwargs: dict = {"quantity": 42 if quantity is None else quantity}

    if food is not None:
        kwargs["food"] = food
    if express is not None:
        kwargs["express"] = express
    if is_awesome is not None:
        kwargs["is_awesome"] = is_awesome

    get_food(**kwargs)


print("\n\nCalling wrapper function 'easy way'...")

print("\nCase 1: No args...")
wrapper_func_easy()

print("\nCase 2: Only first arg...")
wrapper_func_easy(quantity=12)

print("\nCase 3: Only first 2 args...")
wrapper_func_easy(quantity=12, food="cheese")

print("\nCase 4: Only first 3 args...")
wrapper_func_easy(quantity=12, food="cheese", express=True)

print("\nCase 5: All 4 args...")
wrapper_func_easy(quantity=12, food="cheese", express=True, is_awesome=True)

print("\nCase 6: Skipping one arg and NOT breaking things...")
wrapper_func_easy(quantity=12, food="cheese", is_awesome=True)
