# Obtain Google OAuth2 Refresh Token

Interactive script that exchanges a Google OAuth2 authorization code for a refresh token. Useful for setting up CI/CD pipelines that need offline access to Google APIs (e.g., Chrome Web Store uploads).

## Usage

```bash
# Run and follow the prompts for client_id, client_secret, and authorization code
python get_refresh_token.py
```
