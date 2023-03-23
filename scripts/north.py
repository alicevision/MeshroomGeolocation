from argparse import ArgumentParser
import data2D
import generateNorth
import logging
import logLevel

# Parsing of all arguments
def buildArgumentParser() -> ArgumentParser:
    ap = ArgumentParser()
    ap.add_argument("--GPSFile", help="GPSFile", type=str)
    ap.add_argument("--outputPath", help="output", type=str)
    ap.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    ap.add_argument("--outputFolder", help="outputFolder", type=str)
    return ap

def main():
    ap = buildArgumentParser()
    args = ap.parse_args()

    logging.basicConfig(level=logLevel.textToLogLevel(args.verboseLevel))

    logging.info("North !")
    # get image to know where is the north
    image = data2D.Map2D(args.GPSFile, args.outputFolder, 550)
    logging.debug(f"Path of Image : {image}")

    generateNorth.generateNorth(image, args.outputFolder, args.output)

    logging.info("North generated")


if __name__ == "__main__":
    main()