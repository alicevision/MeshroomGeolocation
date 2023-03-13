import laspy
import os
from argparse import ArgumentParser
import shutil
import logging
import mergeAsciiTiles
import convertWgs84ToLambert93
import logLevel

#TODO logging
# Parsing of all arguments
def buildArgumentParser() -> ArgumentParser:
    ap = ArgumentParser()
    ap.add_argument("--folder", help="input folder", type=str)
    ap.add_argument("--GPSFile", help="gps data file", type=str)
    ap.add_argument("--verboseLevel", help="verbose level for logging", type=str)
    ap.add_argument("--outputFolder", help="output folder", type=str)
    return ap

# Append a las file to another las file
def append_to_las(in_las, out_las):
    with laspy.open(out_las, mode='a') as outlas:
        with laspy.open(in_las) as inlas:
            for points in inlas.chunk_iterator(2_000_000):
                outlas.append_points(points)

# Merge all las files in a folder
def mergeLAS(InputFolder, OutputFolder):
    try:
        logging.info('Running Merge LAS')

        #This is the las file to append to.  DO NOT STORE THIS FILE IN THE SAME DIRECTORY AS BELOW...
        out_las = os.path.join(OutputFolder, "merge.las")

        logging.debug(f"Merged file: {out_las}")

        # Writing to sample.json
        open(out_las, "x")

        for (dirpath, dirnames, filenames) in os.walk(InputFolder):
            count = 0
            logging.debug(f"Dir Path : {dirpath}")
            for file in filenames:
                if file.endswith('.las') and count == 0:
                    logging.debug("Copy first las file")
                
                    # Specify the file to be copied and the destination
                    src_file = os.path.join(dirpath, file)
                    print(src_file)
                    dst_file = out_las

                    # Copy the file
                    shutil.copy(src_file, dst_file)
                    count+=1
                elif file.endswith('.las'):
                    logging.debug("Append las file")
                    in_las = os.path.join(dirpath, file)
                    append_to_las(in_las, out_las)
                    count+=1  
        logging.debug('Finished without errors - merge_LAS.py')
    except:
        logging.error('Error in append las')


def main():
    ap = buildArgumentParser()
    args = ap.parse_args()

    logging.basicConfig(level=logLevel.textToLogLevel(args.verboseLevel))

    logging.info("Merge !")

    for (dirpath, dirnames, filenames) in os.walk(args.folder):
        for inFile in filenames:
            if inFile.endswith('.las'):
                # Merge all las files in a file
                mergeLAS(args.folder, args.outputFolder)
                break

            elif inFile.endswith('.asc'):
                lambertData = convertWgs84ToLambert93.convertGPSDataToLambert93(args.GPSFile)

                # Merge all asc files in a file
                mergeAsciiTiles.mergeASCII(args.folder, args.outputFolder, lambertData)
                break
    
    logging.info("Merge Done")


if __name__ == "__main__":
    main()