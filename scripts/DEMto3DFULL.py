import requests
from argparse import ArgumentParser
import math
from math import *
import numpy as np
import rasterio
import trimesh
import logging
import logLevel
import OSMBuildings

# Parsing of all arguments
def buildArgumentParser() -> ArgumentParser:
    ap = ArgumentParser()
    ap.add_argument("--method", help="method of getting gps data", type=str)
    ap.add_argument("--GPSFile", help="GPS file", type=str)
    ap.add_argument("--latInputPoint", help="latitude custom", type=str)
    ap.add_argument("--lonInputPoint", help="longitude custom", type=str)
    ap.add_argument("--kilometers", help="kilometers around point", type=float)
    ap.add_argument("--scale", help="scale of the resulted mesh", type=float)
    ap.add_argument("--verticalTranslation", help="vertical translation for the mesh", type=float)
    ap.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    ap.add_argument("--output", help="output file for the mesh", type=str)
    ap.add_argument("--outputFolder", help="output folder to save the raster", type=str)
    return ap

def internetRequestSRTM(north, south, east, west):
    url = 'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south='+south+'&north='+north+'&west='+west+'&east='+east+'&outputFormat=GTiff&API_Key=b3aae2cb0f7c823f84f2d2e98651c906'
    return requests.get(url)

def calculateFaces(nrows, ncols):
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

def main():
    ap = buildArgumentParser()
    args = ap.parse_args()

    logging.basicConfig(level=logLevel.textToLogLevel(args.verboseLevel))

    logging.info("Elevation map !")

    latitude, longitude = OSMBuildings.coordinatesToUse(args.method, args)

    #conversion of the longitude and latitude into tiles
    offset = args.kilometers * 1.0 / 1000  # why not modify
    north = latitude + offset #north
    south = latitude - offset #south

    lngOffset = offset * math.cos(latitude * math.pi / 180.0)
    east = longitude + lngOffset #east
    west = longitude - lngOffset #west

    #convert float to string
    north = str(north)
    south = str(south)
    east = str(east)
    west = str(west)

    logging.debug(f"{north=} \n {south=} \n {east=} \n {west=}")

    #request to the API
    response = internetRequestSRTM(north, south, east, west)
    open(args.outputFolder +'raster2.tif','wb').write(response.content)

    #read the raster
    with rasterio.open(args.outputFolder +"raster2.tif") as src:
        elev = src.read(1)
    nrows, ncols = elev.shape

    #scale and translation
    x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
    z = elev / 30

    #centrage du mesh
    x -= int(ncols/2)
    y -= int(nrows/2)

    x = x * args.scale 
    y = y * args.scale 
    z = z * args.scale 

    # TODO : calculer la translation en fonction de la distance entre les points
    z = z - args.verticalTranslation

    # Calculates vertices and faces to mesh
    vertices = np.dstack((x, z, -y)).reshape((-1, 3))

    faces = calculateFaces(nrows, ncols)

    outMesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    outMesh.export(args.output)

    logging.info("Elevation map generated")

if __name__ == "__main__":
    main()