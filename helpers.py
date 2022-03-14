from datetime import timedelta
import time

INTEGER_ROUND = 5
WEEK_DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def get_daily(yearly):
    return yearly / 365

def m_to_miles(m):
    return m / 1609.344

def seconds_to_hours(s):
    return s / 3600

def mph_to_pace(mph):
    if mph == 0: return 0
    pace = 60 / mph
    minutes = round(pace)
    seconds = round((pace - minutes) * 60) 
    return str(minutes) + ":" + str(seconds)