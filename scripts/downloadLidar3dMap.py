from argparse import ArgumentParser
import logging
import convert_wgs84_to_lambert93
import download_lidar_from_csv
import log_level

def build_argument_parser() -> ArgumentParser:
    '''Builds the argument parser for the script'''
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--GPSFile", help="GPSFile", type=str)
    argument_parser.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    argument_parser.add_argument("--outputFolder", help="outputFolder", type=str)
    return argument_parser

def main():
    args = build_argument_parser()
    args = args.parse_args()

    logging.basicConfig(level=log_level.text_to_log_level(args.verboseLevel))

    logging.info("3D Map !")
    logging.info("Get Lidar Data")

    # Convert GPS coordinates to Lambert 93
    # Because the Lidar Data only works with Lambert 93 coordinates
    lambert_coordinates = convert_wgs84_to_lambert93.convert_gps_data_to_lambert93(args.GPSFile)
    logging.debug(f"Lambert Coordinates : {lambert_coordinates}")

    downloaded_data = download_lidar_from_csv.download(lambert_coordinates, args.outputFolder)
    logging.debug(f"Tile downloaded : {downloaded_data}")

    logging.info("3D Map infos downloaded")


if __name__ == "__main__":
    main()
