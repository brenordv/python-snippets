"""Example 2: CEP lookup with status-code validation.

Builds on example 1 by checking the HTTP status code before parsing JSON.
"""

import requests

BASE_URL = "https://viacep.com.br/ws/{}/json/"
DEFAULT_CEP = "30170010"  # Google's office in Belo Horizonte, MG, Brazil.


def lookup_cep(cep: str) -> dict | None:
    """Fetch address data for a given CEP, returning None on failure.

    Args:
        cep: An 8-digit Brazilian postal code (digits only).

    Returns:
        A dict with address data, or None if the request failed.
    """
    response = requests.get(BASE_URL.format(cep))
    if response.status_code == 200:
        return response.json()

    print(f"Something went wrong.\nStatus code: {response.status_code}")
    print(
        f"More info: https://www.google.com/search?q=http+status+code+{response.status_code}"
    )
    return None


if __name__ == "__main__":
    data = lookup_cep(DEFAULT_CEP)
    if data:
        print(data)
