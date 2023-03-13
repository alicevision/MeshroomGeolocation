import osmnx as ox
import matplotlib.pyplot as plt
import math
import logging
import json
import os

def convertDistanceToDecimalGPS(dist, lat, lon):
    # initial latitude and longitude (in degrees)
    lat = lat
    lon = lon

    # distance to extend in each direction (in meters)
    d = dist

    # radius of the Earth (in meters)
    R = 6371000

    # convert latitude and longitude to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    # calculate the latitudes and longitudes of the north and south points
    lat_north_rad = math.asin(math.sin(lat_rad) * math.cos(d/R) + math.cos(lat_rad) * math.sin(d/R) * math.cos(0))
    lat_south_rad = math.asin(math.sin(lat_rad) * math.cos(d/R) - math.cos(lat_rad) * math.sin(d/R) * math.cos(0))

    # calculate the latitudes and longitudes of the east and west points
    lon_east_rad = lon_rad + math.atan2(math.sin(90) * math.sin(d/R) * math.cos(lat_rad), math.cos(d/R) - math.sin(lat_rad) * math.sin(lat_north_rad))
    lon_west_rad = lon_rad + math.atan2(math.sin(-90) * math.sin(d/R) * math.cos(lat_rad), math.cos(d/R) - math.sin(lat_rad) * math.sin(lat_north_rad))

    # convert all latitudes and longitudes back to degrees
    lat_north = math.degrees(lat_north_rad)
    lat_south = math.degrees(lat_south_rad)
    lon_east = math.degrees(lon_east_rad)
    lon_west = math.degrees(lon_west_rad)

    # determine the bounds of the bounding box
    north = max(lat_north, lat_south)
    south = min(lat_north, lat_south)
    east = max(lon_east, lon_west)
    west = min(lon_east, lon_west)

    logging.info(f"North: {north:.6f}")
    logging.info(f"South: {south:.6f}")
    logging.info(f"East: {east:.6f}")
    logging.info(f"West: {west:.6f}")

    return (south, north, east, west)

def obtainRoads(center, distance, boolTexts, ax):
    # Fetch OSM street network from the location
    graph = ox.graph_from_point(center,dist=distance, dist_type="bbox")

    # Retrieve nodes and edges
    nodes, edges = ox.graph_to_gdfs(graph)

    # Plot street edges
    edges.plot(ax=ax, edgecolor='#BC8F8F')

    if boolTexts:
        for _, edge in ox.graph_to_gdfs(graph, nodes=False).fillna('').iterrows():
            c = edge['geometry'].centroid
            text = edge['name']
            ax.annotate(text, (c.x, c.y), color="w", size=3)

def obtainBuildings(center, distance, ax):
    # Retrieve buildings
    buildings = ox.geometries_from_point(center, tags={'building':True},dist=distance) 

    # Plot buildings
    buildings.plot(ax=ax, facecolor='khaki', alpha=0.7)

def obtainWater(center, distance, ax):
    # Retrieve water
    water = ox.geometries_from_point(center, tags={'natural':"water"},dist=distance) 

    # Plot water
    water.plot(ax=ax)


def Map2D(GPSData, distance, outputFolder, wantedLayers, roadsNameBool:str):
    # Specify the name that is used to search for the data and the distance from the point

    # Opening JSON file
    with open(GPSData, 'r') as inputfile:
        # Reading from json file
        gpsData = json.load(inputfile)

    place_point = (gpsData["latitude"], gpsData["longitude"])

    distance = int(distance)

    # All wanted layers
    boolRoads = 'boolRoads' in wantedLayers
    boolBuildings = 'boolBuildings' in wantedLayers
    boolWater = 'boolWater' in wantedLayers
    boolNameRoads = roadsNameBool.lower() == 'true'

    fig, ax = plt.subplots(figsize = (4, 4))

    # Try to calculate the bounds
    down, up, right, left = convertDistanceToDecimalGPS(distance, place_point[0], place_point[1])

    ax.set_xlim(left, right)
    ax.set_ylim(down, up)

    #  Removing axis
    ax.set_axis_off()
    ax.margins(0)
    ax.set_in_layout(False)
    fig.tight_layout(pad = 0)

    # Process all layers
    if boolBuildings : obtainBuildings(place_point, distance, ax) 
    if boolWater : obtainWater(place_point, distance, ax)
    if boolRoads : obtainRoads(place_point, distance, boolNameRoads, ax) 


    finalFp = os.path.join(outputFolder, "map2D.png")
    # Save file
    fig.savefig(finalFp, dpi=300, pad_inches = 0, transparent=True)

    return finalFp