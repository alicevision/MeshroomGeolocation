import os
import json
import logging
import math
import osmnx as ox
import matplotlib.pyplot as plt

def convert_distance_to_decimal_gps(distance, lat, lon):
    '''Converts a distance to a decimal GPS coordinate'''
    # Radius of the Earth (in meters)
    radius = 6371000

    # Convert latitude and longitude to radians
    lat_rad = math.radians(lat)
    lon_rad = math.radians(lon)

    # Calculate the latitudes and longitudes of the north and south points
    lat_north_rad = math.asin(math.sin(lat_rad) * math.cos(distance/radius)
                            + math.cos(lat_rad) * math.sin(distance/radius) * math.cos(0))
    lat_south_rad = math.asin(math.sin(lat_rad) * math.cos(distance/radius)
                            - math.cos(lat_rad) * math.sin(distance/radius) * math.cos(0))

    # Calculate the latitudes and longitudes of the east and west points
    lon_east_rad = lon_rad + math.atan2(math.sin(90) * math.sin(distance/radius) * math.cos(lat_rad),
                                        math.cos(distance/radius) - math.sin(lat_rad) * math.sin(lat_north_rad))
    lon_west_rad = lon_rad + math.atan2(math.sin(-90) * math.sin(distance/radius) * math.cos(lat_rad),
                                        math.cos(distance/radius) - math.sin(lat_rad) * math.sin(lat_north_rad))

    # Convert all latitudes and longitudes back to degrees
    lat_north = math.degrees(lat_north_rad)
    lat_south = math.degrees(lat_south_rad)
    lon_east = math.degrees(lon_east_rad)
    lon_west = math.degrees(lon_west_rad)

    # Determine the bounds of the bounding box
    north = max(lat_north, lat_south)
    south = min(lat_north, lat_south)
    east = max(lon_east, lon_west)
    west = min(lon_east, lon_west)

    logging.info(f"North: {north:.6f}")
    logging.info(f"South: {south:.6f}")
    logging.info(f"East: {east:.6f}")
    logging.info(f"West: {west:.6f}")

    return (south, north, east, west)

def obtain_roads(center, distance, texts_wanted, ax):
    '''Obtain roads from the center point with a certain distance and plot them on the map'''
    try:
        # Fetch OSM street network from the location
        graph = ox.graph_from_point(center,dist=distance, dist_type="bbox")

        # Retrieve nodes and edges
        nodes, edges = ox.graph_to_gdfs(graph)

        # Plot street edges
        edges.plot(ax=ax, edgecolor='#BC8F8F')

        logging.debug(f"Texts wanted: {texts_wanted}")

        if texts_wanted is True:
            for _, edge in ox.graph_to_gdfs(graph, nodes=False).fillna('').iterrows():
                c = edge['geometry'].centroid
                text = edge['name']
                ax.annotate(text, (c.x, c.y), color="w", size=3)
    except:
        logging.info("No roads found")

def obtain_buildings(center, distance, ax):
    try:
        # Retrieve buildings
        buildings = ox.features_from_point(center, tags={'building':True},dist=distance)

        # Plot buildings
        buildings.plot(ax=ax, facecolor='khaki', alpha=0.7)
    except:
        logging.info("No buildings found")

def obtain_water(center, distance, ax):
    try:
        # Retrieve water
        water = ox.features_from_point(center, tags={"natural":"water"},dist=distance)

        # Plot water
        water.plot(ax=ax)
    except:
        logging.info("No water found")


def Map2D(gps_data, distance, output_folder, wanted_layers=None, roads_name_wanted=False):
    # Specify the name that is used to search for the data and the distance from the point

    # Opening JSON file
    with open(gps_data, 'r') as input_file:
        # Reading from json file
        json_object = json.load(input_file)

    place_point = (json_object["latitude"], json_object["longitude"])

    distance = int(distance)

    # All wanted layers
    if wanted_layers is None:
        wanted_layers = []
    roads_wanted = 'boolRoads' in wanted_layers
    buildings_wanted = 'boolBuildings' in wanted_layers
    water_wanted = 'boolWater' in wanted_layers

    fig, ax = plt.subplots(figsize = (4, 4))

    # Try to calculate the bounds
    down, up, right, left = convert_distance_to_decimal_gps(distance, place_point[0], place_point[1])

    ax.set_xlim(left, right)
    ax.set_ylim(down, up)

    #  Removing axis
    ax.set_axis_off()
    ax.margins(0)
    ax.set_in_layout(False)
    fig.tight_layout(pad = 0)

    # Process all layers
    if buildings_wanted:
        obtain_buildings(place_point, distance, ax)
    if water_wanted:
        obtain_water(place_point, distance, ax)
    if roads_wanted:
        obtain_roads(place_point, distance, roads_name_wanted, ax)


    final_filepath = os.path.join(output_folder, "map2D.png")
    # Save file
    fig.savefig(final_filepath, dpi=300, pad_inches = 0, transparent=True)

    return final_filepath
