#
# Code is taken from https://medium.com/swlh/using-python-to-connect-to-stravas-api-and-analyse-your-activities-dummies-guide-5f49727aac86
#
# Instructions:
#
# Go to this url:
# http://www.strava.com/oauth/authorize?client_id=[REPLACE_WITH_YOUR_CLIENT_ID]&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=profile:read_all,activity:read_all
# Exchanging [REPLACE_WITH_YOUR_CLIENT_ID] with your client id
# After the page loads you will be redirected to
# http://localhost/exchange_token?state=&code=[THIS_IS_THE_CODE_YOU_NEED_TO_COPY]&scope=read,activity:read_all,profile:read_all
# Put [THIS_IS_THE_CODE_YOU_NEED_TO_COPY] in the command line arguments
# 
# Run this once then the tokens automatically update
# 


import requests
import json
import time
import sys
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
            'code': sys.argv[1], # This is where the code will go
            'grant_type': 'authorization_code',
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