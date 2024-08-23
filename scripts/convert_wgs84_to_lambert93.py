import json
from pyproj import Transformer

def convert_gps_data_to_lambert93(gps_data):
    '''Convert GPS coordinates to Lambert 93 via pyproj'''
    # Opening JSON file
    with open(gps_data, 'r') as input_file:
        # Reading from json file
        json_object = json.load(input_file)

    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

    # Convert GPS coordinates to Lambert 93 via pyproj
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x, y = transformer.transform(latitude, longitude)

    # Data to return
    return {
        "latitude": x,
        "longitude": y
    }
