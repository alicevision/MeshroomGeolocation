from pathlib import Path
import trimesh
from PIL import Image

def generate_plane(texture_path, output_folder, output, distance):
    # Needs distance to right scale the plane
    distance = int(distance)

    texture_path = Path(texture_path).resolve()

    parent_path = Path(__file__).parent.resolve()
    output_folder_path = parent_path / output_folder

    # Collect informations where to save the exported plane
    output_folder_path.mkdir( exist_ok=True)
    obj_path = output
    mtl_path = output_folder_path / 'mltFile.mtl'

    image = Image.open(texture_path)

    # Create plane with corresponding vertices
    plane = trimesh.Trimesh(
        vertices=[[-distance, 0, distance], [distance, 0, distance], [distance, 0, -distance], [-distance, 0, -distance]],
        faces=[[0, 1, 2], [0, 2, 3]],
    )

    # assign material using texture and uv coordinates
    plane.visual = trimesh.visual.texture.TextureVisuals(uv=[[0,0], [1,0], [1, 1], [0, 1]],
                                                         image=image)
    plane.visual.material.name = "mapMat"

    with open(obj_path, 'w') as file:
        plane.export(
            file,
            file_type='obj',
            include_texture=True,
            mtl_name=mtl_path.name,
            resolver=trimesh.visual.resolvers.FilePathResolver(mtl_path)
        )