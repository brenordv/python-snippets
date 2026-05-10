"""Example 1: Basic address lookup from a Brazilian CEP (postal code) via API.

Uses the ViaCEP public API to fetch address data. This first example is the
simplest form -- fire a GET request and print the JSON response.
"""

import requests

BASE_URL = "https://viacep.com.br/ws/{}/json/"
DEFAULT_CEP = "30170010"  # Google's office in Belo Horizonte, MG, Brazil.


def lookup_cep(cep: str) -> dict:
    """Fetch address data for a given CEP number.

    Args:
        cep: An 8-digit Brazilian postal code (digits only).

    Returns:
        A dict with the address information.
    """
    response = requests.get(BASE_URL.format(cep))
    return response.json()


if __name__ == "__main__":
    data = lookup_cep(DEFAULT_CEP)
    print(data)
