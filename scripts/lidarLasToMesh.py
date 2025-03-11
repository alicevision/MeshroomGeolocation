from argparse import ArgumentParser
import os
import logging
import convert_wgs84_to_lambert93
import map_to_mesh
import log_level

def build_argument_parser() -> ArgumentParser:
    '''Builds the argument parser for the script'''
    argument_parser = ArgumentParser()
    argument_parser.add_argument("--folder", help="input folder", type=str)
    argument_parser.add_argument("--GPSFile", help="input gps data", type=str)
    argument_parser.add_argument("--MeshMethod", help="mesh method", type=str)
    argument_parser.add_argument("--dist", help="distance", type=int)
    argument_parser.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    argument_parser.add_argument("--outputobj", help="output obj generated", type=str)
    return argument_parser

def main():
    args = build_argument_parser()
    args = args.parse_args()

    logging.basicConfig(level=log_level.text_to_log_level(args.verboseLevel))

    logging.info("Mesh 3D !")

    lambert_data = convert_wgs84_to_lambert93.convert_gps_data_to_lambert93(args.GPSFile)
    logging.debug(f"Lambert Data : {lambert_data}")

    logging.info(f"Mesh method: {args.MeshMethod}")

    # for each file in the folder find las or asc file and mesh it
    for (dirpath, _, filenames) in os.walk(args.folder):
        for filename in filenames:
            if filename.endswith(".copc.laz"):
                map_to_mesh.meshing(os.path.join(dirpath +"/"+filename), args.dist, args.MeshMethod, lambert_data, args.outputobj)
                break

    logging.info("Mesh 3D done")


if __name__ == "__main__":
    main()
