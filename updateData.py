import requests
import time
from datetime import datetime
import json
import pandas as pd
import matplotlib.pylab as plt
import os
from helpers import m_to_miles, INTEGER_ROUND, seconds_to_hours

lastmodified = os.stat('strava_activities.csv').st_mtime
if lastmodified < time.mktime(datetime.today().timetuple()) - 86400:
    
    # Update credentials if there are expired
    import getTokens

    # Open the credentials file
    with open('strava_tokens.json') as json_file:
        strava_tokens = json.load(json_file)

    # Initial values to get data
    url = "https://www.strava.com/api/v3/athlete/activities"
    access_token = strava_tokens['access_token']

    # Set up pandas dataframe
    activities = pd.DataFrame(
        columns = [
                "id",
                "Name",
                "Start Date Local",
                "Type",
                "Distance",
                "Moving Time",
                "Elapsed Time",
                "Total Elevation Gain",
                "End Latitude / Longitude",
                "External ID",
                "Speed",
                "Avg Heartrate",
                "Max Heartrate"
        ]
    )

    # Get data

    page = 1
    while True:
        r = requests.get(url + '?access_token=' + access_token + '&per_page=200' + '&page=' + str(page))
        r = r.json()
        if (not r):
            break
        
        for x in range(len(r)):
            miles = m_to_miles(r[x]['distance'])
            speed = miles / seconds_to_hours(r[x]['moving_time'])
            page_index = (page - 1) * 200
            
            #
            # Moving time and elapsed times are in seconds
            # Distance is converted to miles
            # Speed is in miles per hour
            # 

            activities.loc[x + page_index,'id'] = r[x]['id']
            activities.loc[x + page_index,'Name'] = r[x]['name']
            activities.loc[x + page_index,'Start Date Local'] = r[x]['start_date_local']
            activities.loc[x + page_index,'Type'] = r[x]['type']
            activities.loc[x + page_index,'Distance'] = round(miles, INTEGER_ROUND)
            activities.loc[x + page_index,'Moving Time'] = r[x]['moving_time']
            activities.loc[x + page_index,'Elapsed Time'] = r[x]['elapsed_time']
            activities.loc[x + page_index,'Total Elevation Gain'] = r[x]['total_elevation_gain']
            activities.loc[x + page_index,'End Latitude / Longitude'] = r[x]['end_latlng']
            activities.loc[x + page_index,'External ID'] = r[x]['external_id']
            activities.loc[x + page_index,'Speed'] = round(speed, INTEGER_ROUND)
            activities.loc[x + page_index,'Avg Heartrate'] = r[x].get('average_heartrate', '0')
            activities.loc[x + page_index,'Max Heartrate'] = r[x].get('max_heartrate', '0')
        page += 1
        
    activities.to_csv('strava_activities.csv')