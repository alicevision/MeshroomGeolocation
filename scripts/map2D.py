from argparse import ArgumentParser
import generatePlane
import logging
import data2D
import logLevel

# Parsing of all arguments
def buildArgumentParser() -> ArgumentParser:
    ap = ArgumentParser()
    ap.add_argument("--GPSFile", help="GPS JSON file", type=str)
    ap.add_argument("--dist", help="distance from center point", type=str)
    ap.add_argument("--layersWanted", help="layers wanted for 2d map", type=str)
    ap.add_argument("--roadsName", help="boolean for name of roads", type=str)
    ap.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    ap.add_argument("--outputPath", help="output file path", type=str)
    ap.add_argument("--outputFolder", help="output folder path", type=str)
    return ap

def main():
    ap = buildArgumentParser()
    args = ap.parse_args()

    logging.basicConfig(level=logLevel.textToLogLevel(args.verboseLevel))

    logging.info("2D Map !")

    # Get image of Open Street Map with corresponding layers
    image = data2D.Map2D(args.GPSFile, args.dist, args.outputFolder, args.layersWanted, args.roadsName)
    logging.debug(f"Path of Image : {image}")

    # Create plane with texture that has been created
    generatePlane.generatePlane(image, args.outputFolder, args.outputPath, args.dist)

    logging.info("2D Map generated")

if __name__ == "__main__":
    main()