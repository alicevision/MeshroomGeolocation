__version__ = "2.0"

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
import os
from pathlib import Path

class MergeLidarLas(desc.CommandLineNode):
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
    targetScriptPath = (currentFileFolderPath / "../../scripts/mergeLidarLas.py").resolve()

    commandLine = pythonPath.as_posix() + ' -E ' + targetScriptPath.as_posix() + ' {allParams}'

    category = 'Geolocation'
    documentation = '''
This node allows to merge LAS files.
'''

    inputs = [
        desc.File(
            name='folder',
            label='Folder',
            description='''Folder''',
            value= "",
        ),
        desc.File(
            name='GPSFile',
            label='GPS File',
            description='''GPS file''',
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
            name='outputFolder',
            label='Output Folder',
            description='''Output folder.''',
            value='{nodeCacheFolder}',
        ),
    ]
