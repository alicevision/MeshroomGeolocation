from argparse import ArgumentParser
import logging
import get_time_dataset
import get_weather
import get_hdri
import log_level

def build_argument_parser() -> ArgumentParser:
    '''Builds the argument parser for the script'''
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--inputFile", help="input SFM data", type=str)
    argument_parser.add_argument("--GPSFile", help="GPSFile", type=str)
    argument_parser.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    argument_parser.add_argument("--output", help="output", type=str)
    return argument_parser

def main():
    args = build_argument_parser()
    args = args.parse_args()

    logging.basicConfig(level=log_level.text_to_log_level(args.verboseLevel))

    logging.info("Weather !")
    time = get_time_dataset.time_of_dataset(args.inputFile, args.GPSFile)
    logging.debug("Time of Dataset : %s", time)

    weather = get_weather.get_weather(args.GPSFile, time)
    logging.debug("Weather : %s", weather)

    get_hdri.get_HDRI(weather, args.output)

    logging.info("Weather HDRI generated")

if __name__ == "__main__":
    main()
