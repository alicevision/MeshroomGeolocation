import requests
import argparse
import math
from math import *
import numpy as np
import rasterio
import trimesh
import json

ap = argparse.ArgumentParser()
ap.add_argument("--method", help="method", type=str)
ap.add_argument("--GPSFile", help="GPSFile", type=str)
ap.add_argument("--latInputPoint", help="latInputPoint", type=str)
ap.add_argument("--lonInputPoint", help="lonInputPoint", type=str)
ap.add_argument("--kilometers", help="kilometers", type=str)
ap.add_argument("--scale", help="scale", type=str)
ap.add_argument("--verticalTranslation", help="verticalTranslation", type=str)
ap.add_argument("--output", help="output", type=str)
ap.add_argument("--outputFolder", help="outputFolder", type=str)
args = ap.parse_args()

#all arguments
method = args.method
GPSauto = args.GPSFile
pointCustom = (float(args.latInputPoint), float(args.lonInputPoint))
kilometers = float(args.kilometers)
scale = float(args.scale)
translation = float(args.verticalTranslation)
finalFp = args.output
folderPath = args.outputFolder

#what method of localisation
if method == "auto":
    # Opening JSON file
    with open(GPSauto, 'r') as inputfile:
    
        # Reading from json file
        json_object = json.load(inputfile)
    
    latitude = json_object["latitude"]
    longitude = json_object["longitude"]

else:
    latitude, longitude = pointCustom

offset = kilometers * 1.0 / 1000  # why not modify
latMax = latitude + offset #north
latMin = latitude - offset #south

lngOffset = offset * math.cos(latitude * math.pi / 180.0)
lngMax = longitude + lngOffset #east
lngMin = longitude - lngOffset #west

#convert float to string
north = str(latMax)
south = str(latMin)
east = str(lngMax)
west = str(lngMin)

url = 'https://portal.opentopography.org/API/globaldem?demtype=SRTMGL1&south='+south+'&north='+north+'&west='+west+'&east='+east+'&outputFormat=GTiff&API_Key=b3aae2cb0f7c823f84f2d2e98651c906'
response = requests.get(url)
open(folderPath +'raster2.tif','wb').write(response.content)

with rasterio.open(folderPath +"raster2.tif") as src:
	elev = src.read(1)
nrows, ncols = elev.shape
x, y = np.meshgrid(np.arange(ncols), np.arange(nrows))
z = elev / 30

#centrage du mesh
x -= int(ncols/2)
y -= int(nrows/2)

xScale = x * scale 
yScale = y * scale 
zScale = z * scale 

zTranslate = zScale - translation

# Calculates vertices and faces to mesh
vertices = np.dstack((xScale, zTranslate, -yScale)).reshape((-1, 3))

faces = []
for r in range(nrows-1):
    for c in range(ncols-1):
        faces.append((
            r * ncols + c,
            r * ncols + c+1,
            (r+1) * ncols + c
        ))
        faces.append((
            r * ncols + c+1,
            (r+1) * ncols + c+1,
            (r+1) * ncols + c
        ))
          
outMesh = trimesh.Trimesh(vertices=vertices, faces=faces)
outMesh.export(finalFp)