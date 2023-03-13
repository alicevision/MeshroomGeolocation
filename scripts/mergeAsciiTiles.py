import numpy as np
import os
import re
import logging

# TODO : add explanation of each function
def getTile(point, scale):
    moduloX = point[0]%scale
    moduloY = point[1]%scale

    tile = [point[0]-moduloX, point[1]+(scale-moduloY)]

    return tile

def getScale(file):
    file = open(file, "r")
    line_cellsize = file.readlines()[4]
    cellsize = line_cellsize.split(" ")
    scale = float(cellsize[-1:][0])

    return scale

def writeHeader(file, merged):
    file = open(file, "r")
    file = file.read()
    lines = [x for x in file.split('\n')]

    sizeCols = lines[2].split(" ")
    xllcorner = float(sizeCols[-1:][0])

    sizeCols = lines[3].split(" ")
    yllcorner = float(sizeCols[-1:][0])

    sizeCols = lines[4].split(" ")
    cellsize = float(sizeCols[-1:][0])

    header = "ncols    %s\n" % merged.shape[1]
    header += "nrows    %s\n" % merged.shape[0]
    header += "xllcorner %s\n" % xllcorner 
    header += "yllcorner %s\n" % yllcorner 
    header += "cellsize %s\n" % cellsize
    header += "NODATA_value -9999"

    return header

def VerticalMergeAscii(tabFiles, count, outputFolder):
    files = [None] * len(tabFiles)
    for i in range (0, len(tabFiles)):
        files[i] = np.loadtxt(tabFiles[i], skiprows=6 )
    
    merged = np.vstack(files)
    
    header = writeHeader(tabFiles[0], merged)

    if not os.path.exists('merge'):
        os.makedirs('merge')
    fp=f"{outputFolder}/vmerged{count}.asc"
    np.savetxt(f"{outputFolder}/vmerged{count}.asc", merged, header=header ,fmt="%3.2f")
    return fp

def HorizontalMergeAscii(tabFiles, outputFolder):
    files = [None] * len(tabFiles)
    for i in range (0, len(tabFiles)):
        files[i] = np.loadtxt(tabFiles[i], skiprows=6 )
    
    merged = np.column_stack(files)

    header = writeHeader(tabFiles[0], merged)

    if not os.path.exists('merge'):
        os.makedirs('merge')
    fp=f"{outputFolder}/merged.asc"
    np.savetxt(f"{outputFolder}/merged.asc", merged, header=header ,fmt="%3.2f")
    return fp

def mergeASCII(inputFolder, outputFolder, lambertData):
    path = r"^(.*_(\d{4})_(\d{4})_.*)$"
    result= []

    # get all files
    for (dirpath, dirnames, filenames) in os.walk(inputFolder):
        logging.debug(f"{dirpath=}")

        # TODO : precise what is done here
        for file in filenames:
            if file.endswith('.asc'):
                result.append(re.search(path, dirpath+"/"+file))
    
    # get source point
    sourcePoint = [lambertData["latitude"]//1000,lambertData["longitude"]//1000]
    logging.debug(f"Point: {sourcePoint}")

    # TODO : for the moment, the dist of merge is set manually here but should be calculated
    dist = 5
    scale = int(getScale(result[0].group(1)))
    logging.debug(f"{scale=}")

    # Get the point of the top left and bottom right of the area to merge
    pointTopLeft = [sourcePoint[0]-dist, sourcePoint[1]+dist]
    pointBottomRight = [sourcePoint[0]+dist, sourcePoint[1]-dist]

    # Get the tile of the top left and bottom right of the area to merge
    tileTopLeft = getTile(pointTopLeft, scale)
    tileBottomRight = getTile(pointBottomRight, scale)

    tiles = []

    # TODO : explain what is done here
    for x in range(tileTopLeft[0], tileBottomRight[0]+scale, scale):
        tilesSameX = []
        for y in range(tileTopLeft[1], tileBottomRight[1]-scale, -scale):
            tilesSameX.append([x, y])

        tiles.append(tilesSameX)

    logging.debug(f"TILES : {tiles}")

    fp = []
    taby = []

    # TODO : explain what is done here
    for tile in tiles:
        fp.append([res.group(1) for res in result if [int(res.group(2)), int(res.group(3))] in tile])
        taby.append([res.group(3) for res in result if [int(res.group(2)), int(res.group(3))] in tile])

    # remove empty lists
    fp = [f for f in fp if f != []]
    taby = [y for y in taby if y != []]

    # reverse order so the order is right for the merge
    for cell in taby:
        cell.sort(reverse = True)
    for cell in fp:
        cell.sort(reverse = True)

    logging.debug(f"{fp=}")
    logging.debug(f"{taby=}")

    # find max length of all tabs
    maxdepth=0
    for cell in taby:
        if (len(cell)>maxdepth):
            maxdepth = len(cell)

    logging.debug(f"max length : {maxdepth}")

    #  fill tabs with -1 value to reach maxlength
    for i in range(len(taby)):
        if (len(taby[i]) < maxdepth) :
            taby[i].append('-1')

    # TODO : explain what is done here
    max_of_rows = []
    for i in range(maxdepth):
        row = []
        for column in taby:
            row.append(column[i])
        max_of_rows.append(max(row))

    # TODO : explain what is done here
    for c in range(len(taby)):
        for r in range(maxdepth):
            if (taby[c][r] < max_of_rows[r]):
                taby[c].insert(r, max_of_rows[r])
                if (int(scale) == 25):
                    fp[c].insert(r, 'external_files/ascii_nodata_25M.asc')
                if (int(scale) == 5):
                    fp[c].insert(r, 'external_files/ascii_nodata_5M.asc')
                if (int(scale) == 1):
                    fp[c].insert(r, 'external_files/ascii_nodata_1M.asc')
                
    logging.debug(f"{fp=}")
    logging.debug(f"{dirpath=}")

    logging.debug("vertical merge \n")
    verticalMergeTab = [None]*len(fp)
    for i in range(len(fp)):
        verticalMergeTab[i] = VerticalMergeAscii(fp[i], i, outputFolder)

    logging.debug(f"{verticalMergeTab=}")

    # TODO : explain what is done here
    finalMerge = HorizontalMergeAscii(verticalMergeTab, outputFolder)

    logging.debug(f"FINAL MERGE : {finalMerge}")