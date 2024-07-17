from pathlib import Path
import trimesh
import numpy as np
from PIL import Image

def generateNorth(OutputFolder, Output):
    parentPath = Path(__file__).parent.resolve()
    outputFolderPath = parentPath / OutputFolder

    outputFolderPath.mkdir( exist_ok=True)
    objPath = Output

    triangle = trimesh.creation.cone(0.5, 2)

    # rotate and translate the triangle so that it is pointing north
    angle = np.deg2rad(180)
    axis = [0, 1, 0]
    rotation_matrix = trimesh.transformations.rotation_matrix(angle, axis)
    translation_matrix = trimesh.transformations.translation_matrix([0, 0, -6])

    triangle.apply_transform(rotation_matrix)
    triangle.apply_transform(translation_matrix)

    triangle.visual = trimesh.visual.color.ColorVisuals(mesh=triangle, vertex_colors=[255, 0, 0, 255])


    # export the triangle to an obj file
    with open(objPath, 'w') as file:
        triangle.export(
            file,
            file_type='obj',
            include_texture=True
        )