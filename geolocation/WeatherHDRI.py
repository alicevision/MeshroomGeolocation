__version__ = "1.2"

import os
from pathlib import Path

from meshroom.core import desc
from meshroom.core.plugin import PluginCommandLineNode, EnvType
class WeatherHDRI(PluginCommandLineNode):
    # Plugin Infos
    envFile = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    envType = EnvType.VENV

    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../scripts/weatherHDRI.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'
    documentation = '''
This node allows to get an HDRI file according to the weather at moment of dataset.
'''

    inputs = [
        desc.File(
            name='inputFile',
            label='SfMData',
            description='''input SfMData.''',
            value= "",
            uid=[0],
        ),
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file.''',
            value= "",
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
            name='output',
            label='Hdri result',
            description='hdri from weather folder',
            value=desc.Node.internalFolder+'hdri.exr',
            semantic="image",
            uid=[],
        ),
    ]
