__version__ = "2.0"

import json
from meshroom.core import desc

class GetGPSData(desc.Node):
    category = 'Geolocation'
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
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (critical, error, warning, info, debug).''',
            value='info',
            values=['critical', 'error', 'warning', 'info', 'debug'],
            exclusive=True,
            uid=[],
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
            chunk.logManager.start(chunk.node.verboseLevel.value)
            chunk.logger.info("GPS")

            # Opening JSON file
            with open(chunk.node.inputFile.value, 'r') as inputFile:
                # Reading from json file
                jsonObject = json.load(inputFile)


            # Create all needed variables
            latitude = []
            latitudeRef = []
            longitude = []
            longitudeRef = []
            decLat = []
            decLon	= []
            latitudeSum = 0
            longitudeSum = 0


            for i in range(len(jsonObject["views"])):
            	# Get the value of lat & long
                latitude.append(jsonObject["views"][i]["metadata"]["GPS:Latitude"])
                latitudeRef.append(jsonObject["views"][i]["metadata"]["GPS:LatitudeRef"])

                longitude.append(jsonObject["views"][i]["metadata"]["GPS:Longitude"])
                longitudeRef.append(jsonObject["views"][i]["metadata"]["GPS:LongitudeRef"])

            	# Get the separation between Degree, Minute, Seconde
                latPoint = [float(x) for x in latitude[i].split(", ")]
                lonPoint = [float(x) for x in longitude[i].split(", ")]

            	# Convert degrees to decimal
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

            chunk.logger.debug("Output: " + str(output))

            # Serializing json
            jsonObject = json.dumps(output, indent=4)

            # Writing to sample.json
            with open(chunk.node.output.value, "w") as outfile:
                outfile.write(jsonObject)

            chunk.logger.info("GPS coordinates saved!")
        finally:
            chunk.logManager.end()
