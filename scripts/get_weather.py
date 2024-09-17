from datetime import datetime
import json
import math
from meteostat import Point, Hourly

def get_weather(gps_data, time_data):
    # Opening JSON file
    with open(gps_data, 'r') as inputfile:
        # Reading from json file
        json_object = json.load(inputfile)

    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

    # get date
    time = time_data["datetime"]

    #add jet lag to time
    offset_time = time_data["offsetTime"]
    time.append(offset_time)

    datefile = tuple(int(element) for element in time)

    year, month, day, hour, minute, second, timezone = datefile

    # Set time period
    ymd = datetime(year, month, day)

    # Create Point from coordinates
    location = Point(latitude, longitude)

    # Get Weather Hourly data from the coordinates
    data = Hourly(location, ymd, ymd)
    data = data.fetch()

    if math.isnan(data['coco'][0]) or math.isnan(data['temp'][0]) or math.isnan(data['rhum'][0]) or math.isnan(data['wdir'][0]) or math.isnan(data['wspd'][0]):
        raise ValueError("No weather data found")

    # Data to return
    return {
        "temperature": data['temp'][0],
        "humidity": data['rhum'][0],
        "wind direction": data['wdir'][0],
        "wind speed": data['wspd'][0],
        "weather condition": (int)(data['coco'][0]),
    }
