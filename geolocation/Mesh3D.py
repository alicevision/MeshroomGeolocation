from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc
import os
from pathlib import Path
class Mesh3D(desc.CommandLineNode):
    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../scripts/mesh3D.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'
    documentation = '''
This node allows to generate a mesh from .asc and .las file.
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
            label='GPS Coordinates',
            description='''GPS coordinates''',
            value= "",
            uid=[0],
        ),
        desc.ChoiceParam(
            name='MeshMethod',
            label='Mesh method',
            description='''Mesh Method (Voxel, Delaunay Triangulation).''',
            value='voxel',
            values=['voxel', 'delaunay'],
            exclusive=True,
            uid=[],
            ),
        desc.IntParam(
            name="dist",
            label="Distance From Center (m)",
            description="Distance from center point (m)",
            value=200,
            range=(50, 2000, 1),
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
            name='outputobj',
            label='OBJ from File',
            description='''OBJ from File''',
            value= desc.Node.internalFolder + "mesh.obj",
            uid=[0],
        ),
    ]