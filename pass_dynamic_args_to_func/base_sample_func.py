"""Shared sample function used by the passing-arguments demos."""


def get_food(
    quantity: int,
    food: str = "Bacon",
    express: bool = True,
    is_awesome: bool = True,
) -> None:
    """Print a mock food order summary."""
    express_msg = "I'm hungry, please hurry!\n" if express else ""
    awesome_msg = "This is awesome!" if is_awesome else "nah..."
    print(f"{express_msg}Here's {quantity} portions of {food}.\n{awesome_msg}")
