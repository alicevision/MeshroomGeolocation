import math
import json

def sunpos(when, location, refraction):
# Extract the passed data
    year, month, day, hour, minute, second, timezone = when
    latitude, longitude = location
# Math typing shortcuts
    rad, deg = math.radians, math.degrees
    sin, cos, tan = math.sin, math.cos, math.tan
    asin, atan2 = math.asin, math.atan2
# Convert latitude and longitude to radians
    rlat = rad(latitude)
    rlon = rad(longitude)
# Decimal hour of the day at Greenwich
    greenwichtime = hour - timezone + minute / 60 + second / 3600
# Days from J2000, accurate from 1901 to 2099
    daynum = (
        367 * year
        - 7 * (year + (month + 9) // 12) // 4
        + 275 * month // 9
        + day
        - 730531.5
        + greenwichtime / 24
    )
# Mean longitude of the sun
    mean_long = daynum * 0.01720279239 + 4.894967873
# Mean anomaly of the Sun
    mean_anom = daynum * 0.01720197034 + 6.240040768
# Ecliptic longitude of the sun
    eclip_long = (
        mean_long
        + 0.03342305518 * sin(mean_anom)
        + 0.0003490658504 * sin(2 * mean_anom)
    )
# Obliquity of the ecliptic
    obliquity = 0.4090877234 - 0.000000006981317008 * daynum
# Right ascension of the sun
    rasc = atan2(cos(obliquity) * sin(eclip_long), cos(eclip_long))
# Declination of the sun
    decl = asin(sin(obliquity) * sin(eclip_long))
# Local sidereal time
    sidereal = 4.894961213 + 6.300388099 * daynum + rlon
# Hour angle of the sun
    hour_ang = sidereal - rasc
# Local elevation of the sun
    elevation = asin(sin(decl) * sin(rlat) + cos(decl) * cos(rlat) * cos(hour_ang))
# Local azimuth of the sun
    azimuth = atan2(
        -cos(decl) * cos(rlat) * sin(hour_ang),
        sin(decl) - sin(rlat) * sin(elevation),
    )
# Convert azimuth and elevation to degrees
    azimuth = into_range(deg(azimuth), 0, 360)
    elevation = into_range(deg(elevation), -180, 180)
# Refraction correction (optional)
    if refraction:
        targ = rad((elevation + (10.3 / (elevation + 5.11))))
        elevation += (1.02 / tan(targ)) / 60
# Return azimuth and elevation in degrees
    return (round(azimuth, 2), round(elevation, 2))


def into_range(x, range_min, range_max):
    shiftedx = x - range_min
    delta = range_max - range_min
    return (((shiftedx % delta) + delta) % delta) + range_min


def getSunPosition3DEnv(GPSFile, TimeData):
    # Opening JSON file
    with open(GPSFile, 'r') as inputfile:
        # Reading from json file
        json_object = json.load(inputfile)
    
    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

    location=(latitude, longitude)

    # get the time data
    datetime = TimeData["datetime"]
    offsetTime = TimeData["offsetTime"]
    datetime.append(offsetTime)

    # Close Encounters latitude, longitude
    when = tuple(int(element) for element in datetime)

    # Get the Sun's apparent location in the sky
    azimuth, elevation = sunpos(when, location, True)

    ##### calculate position of the sun according to azimuth and elevation
    earthSunDistance = 150000000 # 1ua
    distance = earthSunDistance/math.sin(elevation)

    # distance² = sol²+earthSunDistance²
    # sol² = distance² - earthSunDistance²
    floorDistance = math.sqrt(math.pow(distance, 2) - math.pow(earthSunDistance, 2))

    # divide by 10^7 to get the distance in meters
    divideFactor = 10000000

    resultDistance = distance/divideFactor
    resultFloorDistance = floorDistance/divideFactor
    resultEarthSunDistance = earthSunDistance/divideFactor

    # Data to be written
    return {
        "azimuth": azimuth,
        "elevation": elevation,
        "earthSun": resultEarthSunDistance,
        "heightFromSun": resultFloorDistance,
        "pointSun": resultDistance 
    }