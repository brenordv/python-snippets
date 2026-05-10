"""Example 5: CEP lookup with comprehensive exception handling.

Builds on example 4 by catching specific request exception types
(ConnectionError, Timeout, HTTPError, TooManyRedirects) individually.
"""

import requests
from requests.exceptions import (
    ConnectionError as ConnError,
    HTTPError,
    RequestException,
    Timeout,
    TooManyRedirects,
)

BASE_URL = "https://viacep.com.br/ws/{}/json/"
DEFAULT_CEP = "30170010"  # Google's office in Belo Horizonte, MG, Brazil.


def lookup_cep(cep: str) -> dict | None:
    """Fetch address data for a given CEP with full error handling."""
    response = requests.get(BASE_URL.format(cep))
    if response.status_code != 200:
        print(f"Something went wrong.\nStatus code: {response.status_code}")
        print(
            f"More info: https://www.google.com/search?q=http+status+code+{response.status_code}"
        )
        return None

    try:
        return response.json()
    except ConnError as exc:
        print("[ERROR!] Connection error. Are you connected to the internet?")
        print(f"\tTechnical details:\n\t{exc}")
    except Timeout as exc:
        print("[ERROR!] Request timed out.")
        print(f"\tTechnical details:\n\t{exc}")
    except HTTPError as exc:
        print(f"[ERROR!] HTTP error. Status code: {response.status_code}")
        print(f"\tTechnical details:\n\t{exc}")
    except TooManyRedirects as exc:
        print("[ERROR!] Too many redirects.")
        print(f"\tTechnical details:\n\t{exc}")
    except RequestException as exc:
        print("[ERROR!] Something went wrong with the request.")
        print(f"\tTechnical details:\n\t{exc}")
    except Exception as exc:
        print("[ERROR!] Unexpected error.")
        print(f"\tTechnical details:\n\t{exc}")

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
