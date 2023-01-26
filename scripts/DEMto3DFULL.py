import requests
import pandas as pd
import math
from math import *
import numpy as np
import rasterio
import mayavi.mlab as mlab
import trimesh
#necessite pyqt5

# récupération des arguments
import sys
import json

#TODO clean

argv = sys.argv
argv = [element if "--" not in element else "" for element in argv]
argv = [x for x in argv if x != ""]

#all arguments
method = argv[1]
GPSauto = argv[2]
pointCustom = (float(argv[3]), float(argv[4]))
kilometers = float(argv[5])
scale = float(argv[6])
translation = float(argv[7])
finalFp = argv[9]
path = argv[10]

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
open(path +'raster2.tif','wb').write(response.content)

mlab.figure('Model 3D')
with rasterio.open(path +"raster2.tif") as src:
	elev = src.read(1)
	#print(elev.shape)
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

mesh = mlab.mesh(xScale,zTranslate,yScale)

mlab.savefig(finalFp)




