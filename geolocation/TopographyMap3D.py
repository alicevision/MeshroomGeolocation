__version__ = "2.0"

import os
from pathlib import Path

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
# from meshroom.core.plugin import EnvType
class TopographyMap3D(desc.CommandLineNode):
    # Plugin Infos for the Plugin System
    # envFile = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    # envType = EnvType.VENV

    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../scripts/DEMto3DFULL.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'

    documentation = '''
This node allows to get SRTM Data represented as a mesh of the localisation.
'''

    inputs = [
        desc.ChoiceParam(
            name='method',
            label='GPS coordinates method',
            description='''GPS coordinates method''',
            value="auto",
            values=["custom", "auto"],
            exclusive=True,
        ),
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file''',
            value= "",
            enabled=lambda node: 'auto' in node.method.value
        ),
        desc.FloatParam(
            name="latInputPoint",
            label="Latitude Input Point",
            description="Latitude of input point to get image.",
            value=33.668,
            range=(-180.0, 180.0, 0.0001),
            enabled=lambda node: 'custom' in node.method.value
        ),
        desc.FloatParam(
            name="lonInputPoint",
            label="Longitude Input Point",
            description="Longitude of input point to get image.",
            value=8.748,
            range=(-90.0, 90.0, 0.0001),
            enabled=lambda node: 'custom' in node.method.value
        ),
        desc.IntParam(
            name="kilometers",
            label="Bounding Box in kilometers",
            description="Bounding Box in kilometers",
            value=100,
            range=(1, 1000, 1),
        ),
        desc.StringParam(
            name="API_Key",
            label="API Key",
            description="API Key",
            value="b3aae2cb0f7c823f84f2d2e98651c906",
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
            name='output',
            label='Output',
            description='''Output.''',
            value= desc.Node.internalFolder + "result.obj",
        ),
        desc.File(
            name='outputFolder',
            label='Output Folder',
            description='''Output Folder''',
            value= desc.Node.internalFolder,
        ),
    ]
