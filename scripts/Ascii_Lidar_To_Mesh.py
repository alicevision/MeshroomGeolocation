import numpy as np
import laspy as lp
import trimesh
import matplotlib.tri as mtri
import re
from math import *
import mergeAsciiTiles
import logging

def getDatasAccordingToFileType(inputFile, dist):
  # if file is lidar
  if inputFile.endswith('.las'):
    point_cloud = lp.read(inputFile)

    #store coordinates in "points"
    points = np.column_stack((point_cloud.x, point_cloud.y, point_cloud.z))
    logging.debug(f"Number of points in original file: {len(points)}")

    bbox_percent = dist/2000 #if we say that a tile is 2km wide

  # if file is ascii
  elif inputFile.endswith('.asc'):
      logging.debug("ASCII File")
      fichier = open(inputFile, "r")
      fichier = fichier.read()
      lines = [x for x in fichier.split('\n')]

      # set regex
      path = r'^.*_(\d{1,2})M_.*$'
      result = re.search(path, inputFile)
      logging.debug(f"Result of regex : {result}")

      # get scale size of ascii file
      scaleSize = int(mergeAsciiTiles.getScale(inputFile))
      logging.debug(f"Scale size : {scaleSize}")

      # get size of array
      sizeCols = lines[0]
      sizeRows = lines[1]

      sizeCols = sizeCols.split(" ")
      sizeCols = int(sizeCols[-1:][0])

      sizeRows = sizeRows.split(" ")
      sizeRows = int(sizeRows[-1:][0])

      # array size calculation
      arraySize = sizeRows * sizeCols
      logging.debug(f"Size of array : {arraySize}")

      x_all = [None] * arraySize
      y_all = [None] * arraySize

      # get corner coordinates
      x_corner = lines[2]
      x_corner = x_corner.split(" ")
      x_corner = float(x_corner[-1:][0])
      y_corner = lines[3]
      y_corner = y_corner.split(" ")
      y_corner = float(y_corner[-1:][0])

      # get all coordinates
      for i in range(arraySize):
        x_all[i] = i*scaleSize%(scaleSize*sizeCols) + x_corner
        y_all[i] = y_corner - ((i//sizeCols)*scaleSize)

      #get z data from ascii file and put it in a single array
      #each line contains 1000 values and there are 1000 lines
      ascii_grid = np.loadtxt(inputFile, skiprows=6)
      z_all = ascii_grid.flatten()

      x_all = np.array(x_all)
      y_all = np.array(y_all)
      points = np.column_stack((x_all, y_all, z_all))

      bbox_percent = dist/(scaleSize*1000)

  return points, bbox_percent

#Define a function that takes as input an array of points, and a voxel size expressed in meters. It returns the sampled point cloud
def grid_subsampling(crop_points, voxel_size):
  non_empty_voxel_keys, inverse, nb_pts_per_voxel= np.unique(((crop_points - np.min(crop_points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
  idx_pts_vox_sorted=np.argsort(inverse)
  voxel_grid={}
  grid_barycenter,grid_candidate_center=[],[]
  last_seen=0

  for idx,vox in enumerate(non_empty_voxel_keys):
    voxel_grid[tuple(vox)]=crop_points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
    grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
    grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)]-np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
    last_seen+=nb_pts_per_voxel[idx]

  return grid_candidate_center

def meshing(inputFile, dist, meshMethod, lambertData, ExportObj):
  logging.debug(f"Input file : {inputFile}")

  points, bbox_percent = getDatasAccordingToFileType(inputFile, dist)

  #get bounding box of all point cloud 
  points_min = np.min(points, axis=0)
  points_max = np.max(points, axis=0)
  bbox_size = points_max - points_min
  logging.debug(f"min={points_min}, max={points_max}, size before={bbox_size}")

  mean = np.mean(points, axis=0)
  logging.debug(f"mean={mean}")

  # get lambert coordinates
  x = lambertData["latitude"]
  y = lambertData["longitude"]

  delta = [0, 0, 0]

  # calculate delta to center point cloud according to mean of all points
  if x > mean[0]:
    delta[0] += abs(x-mean[0])
  else :
    delta[0] -= abs(x-mean[0])

  if y > mean[1]:
    delta[1] += abs(y-mean[1])
  else :
    delta[1] -= abs(y-mean[1])

  # TODO check for ASCII merged
  # if input_file.endswith('.asc'):
  #   delta[1] = -delta[1]

  #delta for las from top left
  #delta for ASC from bottom left
  if inputFile.endswith('.las'):
    mean = mean + delta

  #crop bounding box and crop point cloud from mean point and bounding box size
  crop_bbox = bbox_size * bbox_percent
  centered_points = points - mean
  logging.debug(f"points centered after : {centered_points}")

  #crop points
  crop_points = [p for p in centered_points if abs(p[0]) < crop_bbox[0] and abs(p[1]) < crop_bbox[1]]
  logging.debug(f"Crop points size: {len(crop_points)}")

  #get x, y and z coordinates from crop_points
  x_all, y_all, z_all = np.hsplit(np.array(crop_points), 3)
  x_all = x_all.flatten()
  y_all = y_all.flatten()
  z_all = z_all.flatten()

  #center z coordinates
  z_elev = z_all[int(len(z_all)/2)]
  z_all = [p - z_elev for p in z_all]
  z_all = np.array(z_all)

  if inputFile.endswith('.asc'):
    meshMethod = "delaunay"
  logging.debug(f"MeshMethod: {meshMethod}")

  # two methods to mesh point cloud
  if meshMethod == 'voxel':
    #store coordinates cropped in crop_points
    crop_points = np.column_stack((x_all, y_all, z_all))
    logging.debug("Number of points in original file:",len(crop_points))

    #change voxel_size to vary subject resolution, it is mesured in meters
    voxel_size=1.5 #determinates the resolution of the mesh
    nb_vox=np.ceil((np.max(crop_points, axis=0) - np.min(crop_points, axis=0))/voxel_size)
    logging.debug("The voxel grid is X,Y,Z voxels:", (nb_vox))

    #reduce resolution through the voxel method
    nb_vox_readout = np.prod(nb_vox, dtype=int) 
    logging.debug("This will reduce number of points to", nb_vox_readout)

    pts_length = len(crop_points)
    perct = ((1-(nb_vox_readout/pts_length))*100)
    logging.debug("Or reduce by", perct, "%")

    #grid sampling
    grid_sampled_point_cloud = grid_subsampling(crop_points, voxel_size)
    grid_sample_pc_np = np.array(grid_sampled_point_cloud)

    #Triangulation from voxel grid
    x_all = grid_sample_pc_np[:,0]
    y_all = grid_sample_pc_np[:,1]
    z_all = grid_sample_pc_np[:,2]

  # for both methods, we need to create a mesh
  tris = mtri.Triangulation(x_all, y_all)
  vertices = np.column_stack((x_all, z_all, -y_all))

  # export mesh
  outMesh = trimesh.Trimesh(vertices=vertices, faces=tris.triangles)
  outMesh.export(ExportObj)