__version__ = "1.0"

from meshroom.core import desc
import os
from pathlib import Path

class MapBuildings(desc.CommandLineNode):
    # On Windows, needs to avoid backslash for command line execution (as_posix needed)
    currentFilePath = Path(__file__).absolute()
    currentFileFolderPath = currentFilePath.parent

    # Get python environnement or global python
    pythonPath = Path(os.environ.get("MESHROOM_GEOLOC_PYTHON", "python"))
    targetScriptPath = (currentFileFolderPath / "../scripts/OSMBuildings.py").resolve()

    commandLine = pythonPath.as_posix() +' '+ targetScriptPath.as_posix() +' {allParams}'

    category = 'Geolocation'
    documentation = '''
        This node displays the 2,5D Map with OSM Buildings data.
    '''
    
    inputs = [
        desc.ChoiceParam(
            name='method',
            label='GPS Coordinates Method',
            description='''Method to get the GPS coordinates''',
            value="auto",
            values=("custom", "auto"),
            exclusive=True,
            uid=[0],
        ),
        desc.File(
            name='GPSFile',
            label='GPS Coordinates File',
            description='''GPS coordinates file''',
            value= "",
            uid=[0],
            enabled=lambda node: 'auto' in node.method.value
        ),
        desc.FloatParam(
            name="latInputPoint",
            label="Latitude Input Point",
            description="Latitude of input point.",
            value=48.85864742340504, 
            range=(-180.0, 180.0, 0.0001),
            uid=[0],
            enabled=lambda node: 'custom' in node.method.value
        ),
        desc.FloatParam(
            name="lonInputPoint",
            label="Longitude Input Point",
            description="Longitude of input point.",
            value=2.3520693092219593,
            range=(-90.0, 90.0, 0.0001),
            uid=[0],
            enabled=lambda node: 'custom' in node.method.value
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
            name='geoJson',
            label='GeoJSON',
            description='''GeoJSON file with data''',
            value= desc.Node.internalFolder + "geojson.geojson",
            uid=[0],
        ),
        desc.File(
            name='outputObj',
            label='Output Obj',
            description='''Output obj generated''',
            value=desc.Node.internalFolder + "result.obj",
            uid=[],
        ),
    ]