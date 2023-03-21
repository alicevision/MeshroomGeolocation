from __future__ import print_function

__version__ = "1.2"

from meshroom.core import desc

class Mesh3D(desc.CommandLineNode):
    commandLine = 'python ./lib/meshroom/nodes/scripts/mesh3D.py {allParams}'

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
            range=(50, 2000, 1.0), # should be more than 30, otherwise doesn't work
            uid=[0],
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