from pyproj import Transformer
import json

def convertGPSDataToLambert93(GPSData):
    # Opening JSON file
    with open(GPSData, 'r') as inputfile:
        # Reading from json file
        json_object = json.load(inputfile)
    
    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

    # Convert GPS coordinates to Lambert 93 via pyproj
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:2154")
    x,y =transformer.transform(latitude, longitude)

    # Data to return
    return {
        "latitude": x,
        "longitude": y
    }