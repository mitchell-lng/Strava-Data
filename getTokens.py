#
# Code is taken from https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86
#

import requests
import json
import time
from decouple import config

# Try to get the current tokens and get expire time
with open('strava_tokens.json') as json_file:
    strava_tokens = json.load(json_file)

# Checks expiration date
if strava_tokens['expires_at'] < time.time():
    response = requests.post(
        url = 'https://www.strava.com/oauth/token',
        data = {
            'client_id': int(config('CLIENT_ID')),
            'client_secret': config('CLIENT_SECRET'),
            'grant_type': 'refresh_token',
            'refresh_token': strava_tokens['refresh_token']
        }
    )

    # Convert to json
    new_strava_tokens = response.json()
    
    # Write new tokens
    with open('strava_tokens.json', 'w') as outfile:
        json.dump(new_strava_tokens, outfile)
    strava_tokens = new_strava_tokens

# Can read?
with open('strava_tokens.json') as check:
  data = json.load(check)