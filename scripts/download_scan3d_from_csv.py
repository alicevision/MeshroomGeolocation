import re
import logging
import requests
import os
from pathlib import Path
import shutil

def download(departementData: dict, Resolution, OutputFolder):
    dp_number = departementData["region"]

    logging.debug(f"Resolution: {int(Resolution)}")

    # Choose the right csv file according to the resolution
    if int(Resolution) == 1: csv_path ='../external_files/RGE_Alti_1m.csv' #default
    if int(Resolution) == 5: csv_path = '../external_files/RGE_Alti_5m.csv'
    if int(Resolution) == 25: csv_path = '../external_files/BD_Alti_25m.csv'
    logging.debug(f"Path : {csv_path}")

    # Get the path of the current file and the parent folder
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    csv = open((currentFileFolderPath / csv_path).resolve(), "r")
    csv = csv.read()
    lines = csv.split('\n')[:-1]

    #  Get infos of all tiles
    path = r'^(\d{1,}(?:[A-Z]?)),(.*[a-zA-Z]),(?:"?)(.*\w).*$'
    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x != None]

    # Use regex to get the right tile
    result = [matchs for matchs in result if (matchs.group(1)) == dp_number]

    for i in range(len(result)):
        # Get all URLs of the right tiles
        links = result[i].group(3).split(',')
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
    
    return OutputFolder+"/"+filename

# Move all asc files from the unzipped folder to the output folder
def extractFromFolder(UnzipPath, OutputFolder):
    for (dirpath, dirnames, filenames) in os.walk(UnzipPath):
        for inFile in filenames:
            if inFile.endswith('.asc'):	
                shutil.move(dirpath + "/" + inFile, OutputFolder+ "/"+ inFile)