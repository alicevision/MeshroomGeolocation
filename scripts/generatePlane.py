from pathlib import Path
import trimesh
from PIL import Image

def generatePlane(TexturePath, OutputFolder, Output, distance):
    # Needs distance to right scale the plane
    distance = int(distance)

    texturePath = Path(TexturePath).resolve()

    parentPath = Path(__file__).parent.resolve()
    outputFolderPath = parentPath / OutputFolder

    # Collect informations where to save the exported plane
    outputFolderPath.mkdir( exist_ok=True)
    objPath = Output
    mtlPath = outputFolderPath / 'mltFile.mtl'

    image = Image.open(texturePath)

    # Create plane with corresponding vertices
    plane = trimesh.Trimesh(
        vertices=[[-distance, 0, distance], [distance, 0, distance], [distance, 0, -distance], [-distance, 0, -distance]],
        faces=[[0, 1, 2], [0, 2, 3]],
    )

    # assign material using texture and uv coordinates
    plane.visual = trimesh.visual.texture.TextureVisuals(uv=[[0,0], [1,0], [1, 1], [0, 1]], image=image)
    plane.visual.material.name = "mapMat"

    with open(objPath, 'w') as file:
        plane.export(
            file,
            file_type='obj',
            include_texture=True,
            mtl_name=mtlPath.name,
            resolver=trimesh.visual.resolvers.FilePathResolver(mtlPath)
        )

    #force add line to .obj because assimp doesn't read last line so miss a face
    file = open(objPath, 'a+')
    file.write('\n')
    file.close()