# -*- coding: utf-8 -*-
import requests
import urllib.parse

"""
Before using this script you must get the authorization code.
You can do this by accessing this url: 
https://accounts.google.com/o/oauth2/auth?client_id=<client_id>&response_type=code&scope=https://www.googleapis.com/auth/chromewebstore&redirect_uri=http://localhost:8818
(remember to add your client_id)

And then get the authorization code (that will be between ?code= and &scope.

Created this snippet so I could use this action in my pipeline: https://github.com/marketplace/actions/chrome-extension-upload-action

PS: If you change the redirect_uri field, remember to update the variable below. 
"""

# Variables
client_id = input('Enter your client id: ').strip()
client_secret = input('Enter your client secret: ').strip()
redirect_uri = 'http://localhost:8818'  # This must match the redirect URI in your Google Cloud Console
code = input('Enter your authorization code: ').strip()

if any([x is None or x == '' for x in [client_id, client_secret, code]]):
    print("You must provide a valid input for all the inputs.")
    exit(1)

# URL encode the parameters
params = urllib.parse.urlencode({
    'client_id': client_id,
    'client_secret': client_secret,
    'code': code,
    'grant_type': 'authorization_code',
    'redirect_uri': redirect_uri
})

# Make the POST request
response = requests.post(f'https://accounts.google.com/o/oauth2/token', data=params, headers={'Content-Type': 'application/x-www-form-urlencoded'})

# Get the JSON response body
json = response.json()

# Check if there's an error
if 'error' not in json:
    print('Your refresh token is:')
    print(json['refresh_token'])
else:
    print('An error occurred:')
    print(json['error'])
