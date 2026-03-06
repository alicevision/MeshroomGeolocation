__version__ = "2.0"

import os
from pathlib import Path

from meshroom.core import desc
from meshroom.core.utils import VERBOSE_LEVEL
# from meshroom.core.plugin import EnvType

class GeolocationLidarLasToMesh(desc.CommandLineNode):
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
    targetScriptPath = (currentFileFolderPath / "../../scripts/lidarLasToMesh.py").resolve()

    commandLine = pythonPath.as_posix() +' -E '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'
    documentation = '''
This node allows to generate a mesh from .asc and .las LIDAR file.
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
            label='GPS Coordinates',
            description='''GPS coordinates''',
            value= "",
        ),
        desc.ChoiceParam(
            name='MeshMethod',
            label='Mesh method',
            description='''Mesh Method (Voxel, Delaunay Triangulation).''',
            value='voxel',
            values=['voxel', 'delaunay'],
            exclusive=True,
            ),
        desc.IntParam(
            name="dist",
            label="Distance From Center (m)",
            description="Distance from center point (m)",
            value=200,
            range=(50, 500, 1),
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
            name='outputobj',
            label='OBJ from File',
            description='''OBJ from File''',
            value='{nodeCacheFolder}/mesh.obj',
        ),
    ]
