from pathlib import Path
import re
import logging
import requests


def get_HDRI(weather_data, output):
    '''Get the HDRI corresponding to the weather condition'''
    # Get weather
    weather = weather_data["weather condition"]

    # Parse csv file
    csv_path ='../external_files/hdri_list.csv'

    # Get the path of the current folder
    current_file_folder_path = Path(__file__).absolute().parent

    with open((current_file_folder_path / csv_path).resolve(), "r") as csv:
        csv = csv.read()

    lines = csv.split('\n')[:-1]

    # Get infos of all hdri
    path = r'^(\d*),(.*),(.*)$'
    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x is not None]

    # Use regex to get the right hdri
    result = [result[i] for i in range(len(result)) if ((int)(result[i].group(1))) == weather]

    url = result[0].group(3)
    response = requests.get(url, stream=True)

    if response.status_code == 200:
        logging.debug("Download started")

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0
        # Write the data to a file
        with open(output, 'wb') as out:
            for data in response.iter_content(block_size):
                wrote = wrote + len(data)
                progress = wrote / total_size * 100
                logging.debug(f"Download Progress: {progress}%")
                out.write(data)
    else:
        logging.error(f"Request failed: {response.status_code}")
