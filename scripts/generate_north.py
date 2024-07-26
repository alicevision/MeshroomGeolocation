from pathlib import Path
import trimesh
import numpy as np

def generate_north(output_folder, output):
    '''Generate the cone pointing north and save it in the output folder as an obj file'''
    parent_path = Path(__file__).parent.resolve()
    output_folder_path = parent_path / output_folder

    output_folder_path.mkdir(exist_ok=True)
    obj_path = output

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
    with open(obj_path, 'w') as file:
        triangle.export(
            file,
            file_type='obj',
            include_texture=True
        )
