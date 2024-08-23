import re
import logging
import math
from pathlib import Path
import os
import requests

def download(lambert93_data, output_folder):
    # Get latitude and longitude from Lambert93Data and convert to kilometers
    x = lambert93_data["latitude"]
    y = lambert93_data["longitude"]

    x = (x / 1000) # Meters to km
    y = (y / 1000)

    logging.debug(f"Latitude and longitude in km : {x}, {y}")

    # Get the closest even number for x and the closest odd number for y to get the right tile
    x = math.floor(x)
    y = math.ceil(y)

    # Get the path of the current file and the parent folder
    current_file_path = Path(__file__).absolute()
    current_file_folder_path = current_file_path.parent

    # Open the file with the URL of all tiles
    with open((current_file_folder_path / "../external_files/TA_diff_pkk_lidarhd.csv").resolve(), "r") as file:
        file = file.read()

    lines = file.split('\n')[:-1]

    # Get infos of all tiles
    path = r"^.*_(\d{4,})_(\d{4,})_.*;(.*).*$"
    result = [re.search(path, line) for line in lines]
    result = [x for x in result if x is not None]

    logging.debug(f"Getting the right tile for x={x} and y={y}")

    # Use regex to get the right tile
    result = [matchs for matchs in result if int(matchs.group(1)) == x and int(matchs.group(2)) == y]

    if len(result) == 0:
        raise Exception("No tile found, please try with other coordinates (available only in France)")

    # Get the URL of the right tile
    tile_url = result[0].group(3)
    logging.debug(f"URL of the right tile : {tile_url}")
    filename = os.path.basename(tile_url)

    logging.debug(f"Archive downloaded : {filename}")

    response = requests.get(tile_url, stream=True)

    if response.status_code == 200:
        logging.info("Download started")

        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024
        wrote = 0
        # As the data is written, the progress is updated
        with open(output_folder+"/"+filename, "wb") as file:
            for data in response.iter_content(block_size):
                wrote = wrote + len(data)
                progress = wrote / total_size * 100
                logging.debug(f"Download Progress: {progress}%")
                # Write the data to a file
                file.write(data)
    else:
        print(f"Request failed: {response.status_code}")

    return output_folder+"/"+filename
