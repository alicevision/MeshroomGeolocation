from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc
import os
from pathlib import Path

class Map2D(desc.CommandLineNode):
    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../scripts/map2D.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'
    
    category = 'Geolocalisation'
    documentation = '''
This node allows to get 2D map of where is the dataset.
'''

    inputs = [
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates contained in JSON file.''',
            value= "",
            uid=[0],
        ),
        desc.IntParam(
            name="dist",
            label="Distance From Input Point",
            description="Distance from input point to get image.",
            value=550,
            range=(250, 2000, 250),
            uid=[0],
        ),
        desc.ChoiceParam(
            name='layersWanted',
            label='Layers Wanted',
            description='All the layers wanted to generate the 2D map.',
            value=['boolBuildings'],
            values=['boolBuildings', 'boolRoads', 'boolWater'],
            exclusive=False,
            uid=[0],
            joinChar=',',
        ),
        desc.BoolParam(
            name='roadsName',
            label='Name of roads',
            description='Name of roads.',
            value=False,
            enabled=lambda node: 'boolRoads' in node.layersWanted.value,
            uid=[0],
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (critical, error, warning, info, debug).''',
            value='info',
            values=['critical', 'error', 'warning', 'info', 'debug'],
            exclusive=True,
            uid=[],
        ),
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output',
            description='''Output''',
            value=desc.Node.internalFolder + "map2D.obj",
            uid=[],
        ),
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value=desc.Node.internalFolder,
            uid=[],
        ),
    ]