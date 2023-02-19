# Meshroom Geolocation
## Install
It is a module for [Meshroom](https://alicevision.org/#meshroom).

You can [download pre-compiled binaries for the latest release](https://github.com/alicevision/meshroom/releases).

Get the source code and install runtime requirements:
```bash
git clone --recursive https://github.com/alicevision/MeshroomGeolocation.git
cd MeshroomGeolocation
pip install -r requirements.txt
```
Custom nodes can be added to Meshroom by setting the environment variable `MESHROOM_NODES_PATH`.

All the nodes will be in Geolocalisation category in Meshroom UI.

## Features
All nodes created by our team enable the following features :
- **GetGPSData** : As its name shows it, it permits to get average GPS data of the dataset. It's useful for all the other features.
- **Map2D** : With this node, you can obtain a 2D map based on [Open Street Map](https://www.openstreetmap.fr/) data. It has several layers of information and a minimal radius precision of 30m.
- **MapBuildings** : The map obtained with this node shows the buildings extruded. It is also based on Open Street Map data.
- **TopographyMap3D** : As we have 2D and 2.5D, this node is good for a worldwide 3D map. It is based on data from NASA of 2000.
- **Map3D** : With this node, a 3D map can be generated, based on IGN data so it's only available for France. Different resolutions can be chosen between 30cm, 1m, 5m and 25m. Corresponding data are downloaded but needs a treatment (Merge and Mesh3D).
- **Merge** : A folder that contains .las or .asc files are merged into a single file to then generate a mesh.
- **Mesh3D** : After treatment, lidar file or ASCII file generates a 3D mesh.
- **North** : As north is not indicated on the maps generated, this node places it as a cone.
- **WeatherHDRI** : As sometimes weather information is needed, HDRI of the current weather of the dataset is downloaded.
- **Sun** : The position of the sun according when the dataset was taken is calculated with thus node and represented as a big yellow sphere.

## Feedback
Do not hesitate to contact us or to give us some feedback.