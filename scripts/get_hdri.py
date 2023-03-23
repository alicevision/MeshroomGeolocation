from pathlib import Path
import re
import logging
import requests


def getHDRI(WeatherData, output):
    # get weather     
    weather = WeatherData["weather condition"]

    #parse csv file
    csv_path ='../external_files/hdri_list.csv'
    
    # Get the path of the current file and the parent folder
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    csv = open((currentFileFolderPath / csv_path).resolve(), "r")
    csv = csv.read()

    lines = csv.split('\n')[:-1]

    # Get infos of all hdri
    path = r'^(\d*),(.*),(.*)$'
    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x != None]

    # Use regex to get the right hdri
    result = [result[i] for i in range(len(result)) if ((int)(result[i].group(1))) == weather]

    URL = result[0].group(3)
    response = requests.get(URL, stream=True)

    if response.status_code == 200:
        logging.debug("Download started")

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0
        # write the data to a file
        with open(output, 'wb') as out:
            for data in response.iter_content(block_size):
                wrote = wrote + len(data)
                progress = wrote / total_size * 100
                logging.debug(f'Download Progress: {progress}%')
                out.write(data)
    else:
        logging.error('Request failed: %d' % response.status_code)