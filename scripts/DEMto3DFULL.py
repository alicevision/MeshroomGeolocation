from argparse import ArgumentParser
import math
import logging
import json
import requests
import numpy as np
import rasterio
import trimesh
import log_level

def build_argument_parser() -> ArgumentParser:
    '''Builds the argument parser for the script'''
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--method", help="method of getting gps data", type=str)
    argument_parser.add_argument("--GPSFile", help="GPS file", type=str)
    argument_parser.add_argument("--latInputPoint", help="latitude custom", type=str)
    argument_parser.add_argument("--lonInputPoint", help="longitude custom", type=str)
    argument_parser.add_argument("--kilometers", help="kilometers around point", type=float)
    argument_parser.add_argument("--API_Key", help="API key", type=str)
    argument_parser.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    argument_parser.add_argument("--output", help="output file for the mesh", type=str)
    argument_parser.add_argument("--outputFolder", help="output folder to save the raster", type=str)
    return argument_parser

def internet_request_SRTM(north, south, east, west, api_key):
    url = "https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south=" + south + "&north=" + north + "&west=" + west + "&east=" + east + "&outputFormat=GTiff&API_Key=" + api_key
    return requests.get(url)

def calculate_faces(nrows, ncols):
    faces = []
    for i in range(0, nrows-1):
        for j in range(0, ncols-1):
            faces.append([
                i*ncols+j,
                i*ncols+j+1,
                (i+1)*ncols+j+1
            ])
            faces.append([
                i*ncols+j,
                (i+1)*ncols+j+1,
                (i+1)*ncols+j
            ])
    return faces

def coordinates_to_use(method, args):
    #what method of localisation
    if method == "auto":
        # Opening JSON file
        with open(args.GPSFile, 'r') as inputfile:
            # Reading from json file
            json_object = json.load(inputfile)

        latitude = json_object["latitude"]
        longitude = json_object["longitude"]

        return (latitude, longitude)
    else:
        return (args.latInputPoint, args.lonInputPoint)

def main():
    args = build_argument_parser()
    args = args.parse_args()

    logging.basicConfig(level=log_level.text_to_log_level(args.verboseLevel))

    logging.info("Elevation map !")

    latitude, longitude = coordinates_to_use(args.method, args)

    #conversion of the longitude and latitude into tiles
    offset = args.kilometers * 1.0 / 1000  # why not modify
    north = latitude + offset #north
    south = latitude - offset #south

    longitude_offset = offset * math.cos(latitude * math.pi / 180.0)
    east = longitude + longitude_offset #east
    west = longitude - longitude_offset #west

    #convert float to string
    north = str(north)
    south = str(south)
    east = str(east)
    west = str(west)

    logging.debug(f"{north=} \n {south=} \n {east=} \n {west=}")

    #request to the API
    response = internet_request_SRTM(north, south, east, west, args.API_Key)
    with open(args.outputFolder +'raster2.tif','wb')as file:
        file.write(response.content)

    # Read the raster
    with rasterio.open(args.outputFolder +"raster2.tif") as file:
        elev = file.read(1)
    nrows, ncols = elev.shape

    # Scale and translation
    x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
    z = elev / 30

    # Center all the mesh
    x -= int(ncols/2)
    y -= int(nrows/2)

    # Center z coordinates
    z_elev = z[int(len(z)/2)]
    z = z - z_elev

    # Calculates vertices and faces to mesh
    vertices = np.dstack((x, z, -y)).reshape((-1, 3))

    faces = calculate_faces(nrows, ncols)

    output_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    output_mesh.export(args.output)

    logging.info("Elevation map generated")

if __name__ == "__main__":
    main()
