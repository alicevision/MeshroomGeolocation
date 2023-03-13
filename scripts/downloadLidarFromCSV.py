import re
import logging
import requests
import os
from pathlib import Path

def download(Lambert93Data, OutputFolder):
    # Get latitude and longitude from Lambert93Data and convert to kilometers
    x = Lambert93Data["latitude"]
    y = Lambert93Data["longitude"]

    x=(x/1000) #meters to km
    y=(y/1000)

    # Get the closest even number for x and the closest odd number for y to get the right tile
    x = int(x) if int(x)%2==0 else int(x)-1
    y = int(y)+2 if int(y)%2!=0 else int(y)+1

    # Get the path of the current file and the parent folder
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    file = open((currentFileFolderPath / "../external_files/TA_diff_pkk_lidarhd.csv").resolve(), "r")
    file = file.read()

    lines = file.split('\n')[:-1]

    # Get infos of all tiles
    path = r"^.*-(\d{4,})_(\d{4,})-\d{4,},(.*).*$"
    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x != None]

    # Use regex to get the right tile
    result = [matchs for matchs in result if int(matchs.group(1)) == x and int(matchs.group(2)) == y]

    # Get the URL of the right tile
    URL = result[0].group(3)
    filename = os.path.basename(URL)

    logging.debug(f"Archive downloaded : {filename}")

    response = requests.get(URL, stream=True)

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
        print('Request failed: %d' % response.status_code)

    return OutputFolder+"/"+filename

    