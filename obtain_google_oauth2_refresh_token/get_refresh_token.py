"""Obtain a Google OAuth2 refresh token from an authorization code.

Before running this script, get an authorization code by visiting:
https://accounts.google.com/o/oauth2/auth?client_id=<YOUR_CLIENT_ID>&response_type=code&scope=https://www.googleapis.com/auth/chromewebstore&redirect_uri=http://localhost:8818

Extract the authorization code from the redirect URL (between ?code= and &scope).

Created to support this GitHub Action:
https://github.com/marketplace/actions/chrome-extension-upload-action
"""

import sys
import urllib.parse

import requests


def get_refresh_token(
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str = "http://localhost:8818",
) -> str:
    """Exchange an authorization code for a refresh token."""
    params = urllib.parse.urlencode({
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
    })

    response = requests.post(
        "https://accounts.google.com/o/oauth2/token",
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=30,
    )

    body = response.json()

    if "error" in body:
        raise RuntimeError(f"OAuth2 error: {body['error']}")

    return body["refresh_token"]


def main() -> None:
    """Prompt for credentials and print the resulting refresh token."""
    client_id = input("Enter your client id: ").strip()
    client_secret = input("Enter your client secret: ").strip()
    code = input("Enter your authorization code: ").strip()

    if not all([client_id, client_secret, code]):
        print("You must provide a valid input for all fields.")
        sys.exit(1)

    try:
        token = get_refresh_token(client_id, client_secret, code)
        print("Your refresh token is:")
        print(token)
    except RuntimeError as exc:
        print(f"An error occurred: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
