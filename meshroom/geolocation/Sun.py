__version__ = "2.0"

import os
from pathlib import Path

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
# from meshroom.core.plugin import EnvType

class Sun(desc.CommandLineNode):
    # Plugin Infos for the Plugin System
    # envFile = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    # envType = EnvType.VENV

    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../../scripts/sun.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'
    documentation = '''
This node allows to display sun according to time and gps.
'''

    inputs = [
        desc.File(
            name='inputFile',
            label='SfMData',
            description='''input SfMData.''',
            value= "",
        ),
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file.''',
            value= "",
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
            value='{nodeCacheFolder}/sun.obj',
        ),
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value='{nodeCacheFolder}',
        ),
    ]
