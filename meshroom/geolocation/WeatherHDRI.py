__version__ = "2.0"

import os
from pathlib import Path

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
# from meshroom.core.plugin import EnvType

class WeatherHDRI(desc.CommandLineNode):
    # Plugin Infos for the Plugin System
    # envFile = os.path.join(os.path.dirname(__file__), '../requirements.txt')
    # envType = EnvType.VENV

    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Resolve venv Python if present, then MESHROOM_GEOLOC_PYTHON, then bare 'python'
    _plugin_dir = (currentFileFolderPath / "../..").resolve()
    _venv_python = next(
        (p for p in [_plugin_dir / ".venv/Scripts/python.exe", _plugin_dir / ".venv/bin/python"] if p.exists()),
        None
    )
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", str(_venv_python) if _venv_python else "python"))
    targetScriptPath = (currentFileFolderPath / "../../scripts/weatherHDRI.py").resolve()

    commandLine = pythonPath.as_posix() +' -E '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'
    documentation = '''
This node allows to get an HDRI file according to the weather of the shooting location based on GPS and time.
'''

    inputs = [
        desc.File(
            name='inputFile',
            label='SfMData',
            description='''input SfMData.''',
            value='',
        ),
        desc.File(
            name='GPSFile',
            label='GPS coordinates file',
            description='''GPS coordinates file.''',
            value='',
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
            label='Hdri result',
            description='hdri from weather folder',
            value='{nodeCacheFolder}/hdri.exr',
            semantic='image',
        ),
    ]
