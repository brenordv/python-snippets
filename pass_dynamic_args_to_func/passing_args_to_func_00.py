"""Demo 0: Basic ways to pass arguments to a function (positional and keyword)."""

from base_sample_func import get_food

print("Just informing the mandatory argument...")
get_food(15)

print("\n\nInforming all arguments by position...")
get_food(2, "Carrots", False, False)

print("\n\nInforming the mandatory argument using its name...")
get_food(quantity=42)

print("\n\nInforming all arguments by name...")
get_food(quantity=2, food="Carrots", express=False, is_awesome=False)
