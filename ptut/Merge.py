from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc
import os
from pathlib import Path
class Merge(desc.CommandLineNode):
    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../scripts/merge.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocalisation'
    documentation = '''
This node allows to merge files to one File.
'''

    inputs = [
        desc.File(
            name='folder',
            label='Folder',
            description='''Folder''',
            value= "",
            uid=[0],
        ),
        desc.File(
            name='GPSFile',
            label='GPS File',
            description='''GPS file''',
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
            name='outputFolder',
            label='Output Folder',
            description='''Output folder.''',
            value= desc.Node.internalFolder,
            uid=[0],
        ),
    ]