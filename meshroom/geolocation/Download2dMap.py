__version__ = "2.0"

import os
from pathlib import Path

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
# from meshroom.core.plugin import EnvType

class Download2dMap(desc.CommandLineNode):
    # Plugin Infos for the Plugin System
    # envFile = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    # envType = EnvType.VENV

    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../../scripts/download2dMap.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'
    documentation = '''
This node allows to get 2D map from GPS coordinates.
'''

    inputs = [
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates contained in JSON file.''',
            value= "",
        ),
        desc.IntParam(
            name="dist",
            label="Distance From Input Point",
            description="Distance from input point to get image.",
            value=550,
            range=(250, 2000, 250),
        ),
        desc.ChoiceParam(
            name='layersWanted',
            label='Layers Wanted',
            description='All the layers wanted to generate the 2D map.',
            value=['boolBuildings'],
            values=['boolBuildings', 'boolRoads', 'boolWater'],
            exclusive=False,
            joinChar=',',
        ),
        desc.BoolParam(
            name='roadsName',
            label='Name of roads',
            description='Name of roads.',
            value=False,
            enabled=lambda node: 'boolRoads' in node.layersWanted.value,
        ),
        desc.ChoiceParam(
            name='verboseLevel',
            label='Verbose Level',
            description='''verbosity level (critical, error, warning, info, debug).''',
            value='info',
            values=VERBOSE_LEVEL,
            exclusive=True,
        ),
    ]

    outputs = [
        desc.File(
            name='outputPath',
            label='Output',
            description='''Output''',
            value='{nodeCacheFolder}/map2D.obj',
        ),
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value='{nodeCacheFolder}',
        ),
    ]
