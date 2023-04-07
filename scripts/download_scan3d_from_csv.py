import re
import logging
import requests
import os
from pathlib import Path
import shutil

currentDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.dirname(currentDir)

def download(departementData: dict, Resolution, OutputFolder):

    logging.debug(f"Resolution: {int(Resolution)}")

    # Choose the right csv file according to the resolution
    if int(Resolution) == 1:
        csv_path = os.path.join(rootDir, 'external_files/RGE_Alti_1m.csv') #default
    elif int(Resolution) == 5:
        csv_path = os.path.join(rootDir, 'external_files/RGE_Alti_5m.csv')
    elif int(Resolution) == 25:
        csv_path = os.path.join(rootDir, 'external_files/BD_Alti_25m.csv')
    else:
        raise RuntimeError(f"Unknown resolution: {Resolution}")
    logging.debug(f"Path: {csv_path}")

    # Get the path of the current file and the parent folder
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent
    logging.debug(f"currentFileFolderPath: {currentFileFolderPath}")
    logging.debug(f"rootDir: {rootDir}")

    csv_fullpath = (currentFileFolderPath / csv_path).resolve()
    logging.debug(f"csv_fullpath: {csv_fullpath}")

    csv = open((currentFileFolderPath / csv_path).resolve(), "r")
    csv = csv.read()
    lines = csv.split('\n')[:-1]

    #  Get infos of all tiles
    path = r'^(\d{1,}(?:[A-Z]?)),(.*[a-zA-Z]),(?:"?)(.*\w).*$'
    allTiles = [re.search(path, line) for line in lines]
    allTiles = [x for x in allTiles if x != None]
    logging.debug(f"Matching lines: {[a.group(1) for a in allTiles]}")

    # Use regex to get the right tile
    dp_number = departementData["region"]
    logging.debug(f"Department number: {dp_number}")
    result = [matchs for matchs in allTiles if (matchs.group(1)) == dp_number]
    if not result:
        raise RuntimeError("No matching tile.")

    filename = ""
    for r in result:
        # Get all URLs of the right tiles
        links = r.group(3).split(',')
        for j in range (len(links)):
            filename = os.path.basename(links[j])
            response = requests.get(links[j], stream=True)

            if response.status_code == 200:
                logging.info("Download started")

                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                wrote = 0
                # As the data is written, the progress is updated
                with open(OutputFolder+"/"+filename, "wb") as f:
                    for data in response.iter_content(block_size):
                        wrote = wrote + len(data)
                        progress = wrote / total_size * 100
                        logging.info(f'Download Progress: {progress}%')
                        # write the data to a file
                        f.write(data)
            else:
                logging.info('Request failed: %d' % response.status_code)

    res = os.path.join(OutputFolder, filename)
    return res

# Move all asc files from the unzipped folder to the output folder
def extractFromFolder(UnzipPath, OutputFolder):
    for (dirpath, dirnames, filenames) in os.walk(UnzipPath):
        for inFile in filenames:
            if inFile.endswith('.asc'):
                shutil.move(os.path.join(dirpath, inFile), os.path.join(OutputFolder, inFile))


