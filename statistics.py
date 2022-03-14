import pandas as pd
from datetime import date, datetime
import time
from helpers import get_daily, mph_to_pace

df = pd.read_csv('strava_activities.csv')

def get_data():
    global df

    df = pd.read_csv('strava_activities.csv')
    df = df.sort_values('Start Date Local')
    df = df.iloc[::-1]

def streak():
    global df

    get_data()

    count = 0

    # Get current date in epoch
    currentdate = time.mktime(date.today().timetuple())

    for index, str_date in zip(df.id, df['Start Date Local']):
        # Get stored date in start date
        start_date = time.mktime(datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%SZ").timetuple())

        if abs(currentdate - start_date) < 86400 * (count + 1):
            count += 1
        else:
            break

    return count

def current_daily_average_365():
    global df

    get_data()
    
    total = 0
    total_speed = 0
    total_distance = 0

    currentdate = time.mktime(date.today().timetuple())

    for index, str_date, distance, speed in zip(df.id, df['Start Date Local'], df['Distance'], df['Speed']):
        start_date = time.mktime(datetime.strptime(str_date, "%Y-%m-%dT%H:%M:%SZ").timetuple())

        if abs(currentdate - start_date) < 31536000:
            total += 1
            total_speed += speed
            total_distance += distance
        else:
            break

    average_speed = total_speed / total    

    return [get_daily(total_distance), mph_to_pace(average_speed)]
