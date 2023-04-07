from argparse import ArgumentParser
import getTimeDataset
import get_weather
import get_hdri
import logging
import logLevel

# Parsing of all arguments
def buildArgumentParser() -> ArgumentParser:
    ap = ArgumentParser()
    ap.add_argument("--inputFile", help="input SFM data", type=str)
    ap.add_argument("--GPSFile", help="GPSFile", type=str)
    ap.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    ap.add_argument("--output", help="output", type=str)
    return ap

def main():
    ap = buildArgumentParser()
    args = ap.parse_args()

    logging.basicConfig(level=logLevel.textToLogLevel(args.verboseLevel))

    logging.info("Weather !")
    time = getTimeDataset.timeOfDataset(args.inputFile, args.GPSFile)
    logging.debug(f"Time of Dataset : {time}")

    weather = get_weather.getWeather(args.GPSFile, time)
    logging.debug(f"Weather : {weather}")

    get_hdri.getHDRI(weather, args.output)

    logging.info("Weather HDRI generated")

if __name__ == "__main__":
    main()