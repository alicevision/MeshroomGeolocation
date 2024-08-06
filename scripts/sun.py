from argparse import ArgumentParser
import logging
import getTimeDataset
import sun_position
import generateSun
import log_level

def build_argument_parser() -> ArgumentParser:
    '''Parsing of all arguments'''
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--inputFile", help="input SFM data", type=str)
    argument_parser.add_argument("--GPSFile", help="GPS file", type=str)
    argument_parser.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    argument_parser.add_argument("--outputPath", help="output path", type=str)
    argument_parser.add_argument("--outputFolder", help="output folder", type=str)
    return argument_parser

def main():
    args = build_argument_parser()
    args = args.parse_args()

    logging.basicConfig(level=log_level.text_to_log_level(args.verboseLevel))

    logging.info("Sun!")
    time = getTimeDataset.timeOfDataset(args.inputFile, args.GPSFile)
    logging.debug("Time of Dataset: %s", time)

    position = sun_position.getSunPosition3DEnv(args.GPSFile, time)
    logging.debug("Sun position: %s", position)

    generateSun.generateSun(args.outputFolder, position)

    logging.info("Sun generated")


if __name__ == "__main__":
    main()
