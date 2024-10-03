from argparse import ArgumentParser
import logging
import generate_plane
import data2D
import log_level

def build_argument_parser() -> ArgumentParser:
    '''Builds the argument parser for the script'''
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--GPSFile", help="GPS JSON file", type=str)
    argument_parser.add_argument("--dist", help="distance from center point", type=str)
    argument_parser.add_argument("--layersWanted", help="layers wanted for 2d map", type=str)
    argument_parser.add_argument("--roadsName", help="boolean for name of roads", type=str)
    argument_parser.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    argument_parser.add_argument("--outputPath", help="output file path", type=str)
    argument_parser.add_argument("--outputFolder", help="output folder path", type=str)
    return argument_parser

def main():
    args = build_argument_parser()
    args = args.parse_args()

    logging.basicConfig(level=log_level.text_to_log_level(args.verboseLevel))

    logging.info("2D Map !")

    # Get image of Open Street Map with corresponding layers
    image = data2D.Map2D(args.GPSFile, args.dist, args.outputFolder, args.layersWanted, args.roadsName)
    logging.debug(f"Path of Image : {image}")

    # Create plane with texture that has been created
    generate_plane.generate_plane(image, args.outputFolder, args.outputPath, args.dist)

    logging.info("2D Map generated")

if __name__ == "__main__":
    main()