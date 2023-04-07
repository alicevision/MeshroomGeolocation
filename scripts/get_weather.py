from datetime import datetime
from meteostat import Point, Hourly
import json

def getWeather(GPSData, TimeData):
    # Opening JSON file
    with open(GPSData, 'r') as inputfile:
        # Reading from json file
        json_object = json.load(inputfile)

    latitude = json_object["latitude"]
    longitude = json_object["longitude"]    

    # get date
    time = TimeData["datetime"]

    #add jet lag to time
    offsetTime = TimeData["offsetTime"]
    time.append(offsetTime)

    datefile = tuple(int(element) for element in time)

    year, month, day, hour, minute, second, timezone = datefile

    # Set time period
    ymd = datetime(year, month, day)

    # Create Point from coordinates
    location = Point(latitude, longitude)

    # Get Weather Hourly data from the coordinates
    data = Hourly(location, ymd, ymd)
    data = data.fetch()

    # Data to return
    return {
        "temperature": data['temp'][0],
        "humidity": data['rhum'][0],
        "wind direction": data['wdir'][0],
        "wind speed": data['wspd'][0],
        "weather condition": (int)(data['coco'][0]),
    }