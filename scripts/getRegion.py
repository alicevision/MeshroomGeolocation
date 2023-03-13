from geopy.geocoders import Nominatim
import json

# Return region number (as string to handle corse) from the postCode
def regionFromPostcode(postCode: int):
    firstTwoNumber = postCode//1000
    # dom tom
    if firstTwoNumber == 97:
        return str(postCode//100)
    # corse
    elif firstTwoNumber == 20:
        return "2A" if postCode < 20200 else "2B"
    else:
        return str(firstTwoNumber)

def getDepartement(GPSData):
    # Opening JSON file
    with open(GPSData, 'r') as GPSfile:
        # Reading from json file
        json_gps = json.load(GPSfile)

    # initialize Nominatim API
    geolocator = Nominatim(user_agent="getRegion")
    # Latitude & Longitude input
    Latitude = json_gps["latitude"]
    Longitude = json_gps["longitude"]
    
    # Reverse Geocoding call
    location = geolocator.reverse(str(Latitude)+","+str(Longitude))

    address = location.raw['address']

    return {
        "region": regionFromPostcode(int(address["postcode"])),
        "postcode": address["postcode"]
    }