from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

import json
import logging

class GetGPSData(desc.Node):
    category = 'Geolocalisation'
    documentation = '''
This node allows to get GPS coordinates of a file.
'''

    inputs = [
        desc.File(
            name='inputFile',
            label='SfMData',
            description='''input SfMData.''',
            value= "",
            uid=[0],
        ),
    ]

    outputs = [
        desc.File(
            name='output',
            label='GPS coordinates',
            description='GPS coordinates from input file',
            value=desc.Node.internalFolder + "gps.json",
            uid=[],
        ),
    ]

    def processChunk(self, chunk):
        try:
            logging.basicConfig(level=logging.INFO)
            logging.info("GPS")

            # Opening JSON file
            with open(chunk.node.inputFile.value, 'r') as inputfile:
                # Reading from json file
                json_object = json.load(inputfile)


            # Create all needed variables
            latitude = []
            latitudeRef = []
            longitude = []
            longitudeRef = []
            decLat = []
            decLon	= []
            latitudeSum = 0
            longitudeSum = 0
            

            for i in range(len(json_object["views"])):
            	#get the value of lat & long
                latitude.append(json_object["views"][i]["metadata"]["GPS:Latitude"])
                latitudeRef.append(json_object["views"][i]["metadata"]["GPS:LatitudeRef"])

                longitude.append(json_object["views"][i]["metadata"]["GPS:Longitude"])
                longitudeRef.append(json_object["views"][i]["metadata"]["GPS:LongitudeRef"])
                
            	#get the separation between Degree, Minute, Seconde
                latPoint = [float(x) for x in latitude[i].split(", ")]
                lonPoint = [float(x) for x in longitude[i].split(", ")]

            	# convert degrees to decimal
            	# Decimal degrees = Degrees + (Minutes/60) + (Seconds/3600)
                decLat.append(latPoint[0] + (latPoint[1]/60) + (latPoint[2]/3600))
                # If north keep the same, otherwise it has to be negative value
                if latitudeRef[i] != "N" :
                    decLat[i]=-decLat[i]
                
                decLon.append(lonPoint[0] + (lonPoint[1]/60) + (lonPoint[2]/3600))
                if longitudeRef[i] != "E" :
                    decLon[i] = -decLon[i]

            # Sum of all latitudes
            for i in range(len(latitude)):
                latitudeSum += decLat[i]
            
            # Sum of all longitudes
            for i in range(len(longitude)):
                longitudeSum += decLon[i]
                
            # Average of latitude and longitude
            latitudeAvg = latitudeSum / len(latitude)
            longitudeAvg = longitudeSum / len(longitude)

            # Data to be written
            output = {
                "latitude": latitudeAvg,
                "longitude": longitudeAvg
            }

            # Serializing json
            json_object = json.dumps(output, indent=4)
            
            # Writing to sample.json
            with open(chunk.node.output.value, "w") as outfile:
                outfile.write(json_object)

        finally:
            chunk.logManager.end()
