import json
from datetime import datetime
from timezonefinder import TimezoneFinder
from dateutil import tz

def time_of_dataset(sfm_data, gps_data):
    # Opening JSON file
    with open(sfm_data, 'r') as input_file:
        # Reading from json file
        json_object = json.load(input_file)

    date = json_object["views"][0]["metadata"]["Exif:DateTimeOriginal"]

    if "Exif:OffsetTimeOriginal" in json_object["views"][0]["metadata"]:
        offset_time = json_object["views"][0]["metadata"]["Exif:OffsetTimeOriginal"]

        # get offset time
        offset_time = offset_time.replace(":", ".")
        offset_time = int(float(offset_time))
    else:
        # Opening JSON file
        with open(gps_data, 'r') as gps_file:
            # Reading from json file
            json_gps = json.load(gps_file)

        timezone = TimezoneFinder().timezone_at(lng=json_gps["longitude"], lat=json_gps["latitude"])

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz(timezone)
        start_date = datetime.strptime(date, "%Y:%m:%d %H:%M:%S")

        # if no offset time, get offset time from GPS coordinates
        start_date = start_date.replace(tzinfo = from_zone)
        local = start_date.astimezone(to_zone)
        local = list(str(local.utcoffset()).split(':'))
        # if first element contains "day", multiply by 24
        if "day" in local[0]:
            local[0] = local[0].replace("day", "")
            day = local[0].split(",")[0]
            hour = local[0].split(",")[1]
            offset_time = int(day) * 24 + int(hour)
        else:
            offset_time = int(local[0])

    date = date.replace(" ", ":")

    date = list(date.split(":"))

    # Data to return
    return {
        "datetime": date,
        "offsetTime": offset_time
    }
