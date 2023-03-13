from argparse import ArgumentParser
import convertWgs84ToLambert93
import downloadLidarFromCSV
import unzip_archive
import LAZtoLAS
import getRegion
import download_scan3d_from_csv
import logging
import logLevel

# Parsing of all arguments
def buildArgumentParser() -> ArgumentParser:
    ap = ArgumentParser()
    ap.add_argument("--GPSFile", help="GPSFile", type=str)
    ap.add_argument("--resolution", help="resolution", type=str)
    ap.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    ap.add_argument("--outputFolder", help="outputFolder", type=str)
    return ap

def main():
    ap = buildArgumentParser()
    args = ap.parse_args()

    logging.basicConfig(level=logLevel.textToLogLevel(args.verboseLevel))

    logging.info("3D Map !")

    if float(args.resolution) == 0.3:
        logging.info(f"Get Lidar Data")

        # Convert GPS coordinates to Lambert 93 because the Lidar Data only works with Lambert 93 coordinates
        lambertCoord = convertWgs84ToLambert93.convertGPSDataToLambert93(args.GPSFile)
        logging.debug(f"Lambert Coordinates : {lambertCoord}")

        fpZipArchive = downloadLidarFromCSV.download(lambertCoord, args.outputFolder)
        logging.debug(f"Zip Archive : {fpZipArchive}")

        fpUnzipArchive = unzip_archive.unzip(fpZipArchive, args.outputFolder)
        logging.debug(f"Unzip Archive : {fpUnzipArchive}")

        # Convert LAZ files to LAS files because LAZ are compressed and cannot be merged and meshed
        LAZtoLAS.convert(fpUnzipArchive, args.outputFolder)

    else :
        logging.info(f"Get RGE or BD Alti Data")

        # Get the departement of the GPS coordinates because the RGE and BD Alti Data only works with departement coordinates
        departementInfo = getRegion.getDepartement(args.GPSFile)
        logging.debug(f"Departement : {departementInfo}")

        fpZipArchive = download_scan3d_from_csv.download(departementInfo, float(args.resolution), args.outputFolder)
        logging.debug(f"Zip Archive : {fpZipArchive}")

        fpUnzipArchive = unzip_archive.unzip(fpZipArchive, args.outputFolder)
        logging.debug(f"Unzip Archive : {fpUnzipArchive}")

        # Move the files from the folder to the output folder
        download_scan3d_from_csv.extractFromFolder(fpUnzipArchive, args.outputFolder)
    
    logging.info("3D Map infos downloaded")


if __name__ == "__main__":
    main()