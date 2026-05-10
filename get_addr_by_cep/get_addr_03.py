"""Example 3: Interactive CEP lookup with user input and validation.

Builds on example 2 by prompting the user for a CEP number in a loop,
validating that the input contains only digits.
"""

import requests

BASE_URL = "https://viacep.com.br/ws/{}/json/"
DEFAULT_CEP = "30170010"  # Google's office in Belo Horizonte, MG, Brazil.


def lookup_cep(cep: str) -> dict | None:
    """Fetch address data for a given CEP, returning None on failure."""
    response = requests.get(BASE_URL.format(cep))
    if response.status_code == 200:
        return response.json()

    print(f"Something went wrong.\nStatus code: {response.status_code}")
    print(
        f"More info: https://www.google.com/search?q=http+status+code+{response.status_code}"
    )
    return None


def main() -> None:
    """Interactive loop: ask user for a CEP and display the address."""
    print("Input your CEP number or press Enter to use our default test value.")
    print("To exit, type -1 and press Enter.")

    while True:
        cep = input("Please, enter your CEP (just numbers): ")

        if cep == "-1":
            print("Cancelling operation.")
            break

        if cep.strip() == "":
            print("Using default test value...")
            cep = DEFAULT_CEP
        elif not cep.isdigit():
            print("Please, enter CEP number... just the numbers.")
            continue

        data = lookup_cep(cep)
        if data:
            print(data)


if __name__ == "__main__":
    main()
