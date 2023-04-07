from argparse import ArgumentParser
import os
import convertWgs84ToLambert93
import Ascii_Lidar_To_Mesh
import logging
import logLevel

# Parsing of all arguments
def buildArgumentParser() -> ArgumentParser:
    ap = ArgumentParser()
    ap.add_argument("--folder", help="input folder", type=str)
    ap.add_argument("--GPSFile", help="input gps data", type=str)
    ap.add_argument("--MeshMethod", help="mesh method", type=str)
    ap.add_argument("--dist", help="distance", type=int)
    ap.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    ap.add_argument("--outputobj", help="output obj generated", type=str)
    return ap

def main():
    ap = buildArgumentParser()
    args = ap.parse_args()

    logging.basicConfig(level=logLevel.textToLogLevel(args.verboseLevel))

    logging.info("Mesh 3D !")

    lambertData = convertWgs84ToLambert93.convertGPSDataToLambert93(args.GPSFile)
    logging.debug(f"Lambert Data : {lambertData}")

    logging.info(f"Mesh method: {args.MeshMethod}")

    # for each file in the folder find las or asc file and mesh it
    for (dirpath, dirnames, filenames) in os.walk(args.folder):
        for inFile in filenames:
            if inFile.endswith('.las') or inFile.endswith('.asc'):
                Ascii_Lidar_To_Mesh.meshing(os.path.join(dirpath +"/"+inFile), args.dist, args.MeshMethod, lambertData, args.outputobj)
                break
    
    logging.info("Mesh 3D done")


if __name__ == "__main__":
    main()