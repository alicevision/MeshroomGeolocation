import logging
import numpy as np
import laspy as lp
import trimesh
import matplotlib.tri as mtri

def get_datas_according_to_file_type(input_file, dist):
    '''As we could have different file types, we need to get the data according to the file type'''
    # if file is lidar COPC
    if input_file.endswith('.copc.laz'):
        point_cloud = lp.read(input_file)

        #store coordinates in "points"
        points = np.column_stack((point_cloud.x, point_cloud.y, point_cloud.z))
        logging.debug(f"Number of points in original file: {len(points)}")

        bbox_percent = dist/1000 #if we say that a tile is 1km wide

    return points, bbox_percent

def grid_subsampling(crop_points, voxel_size):
    '''
    Define a function that takes as input an array of points, and a voxel size expressed in meters.
    It returns the sampled point cloud
    '''
    non_empty_voxel_keys, inverse, nb_pts_per_voxel= np.unique(((crop_points - np.min(crop_points, axis=0)) // voxel_size).astype(int), axis=0, return_inverse=True, return_counts=True)
    idx_pts_vox_sorted=np.argsort(inverse)
    voxel_grid={}
    grid_barycenter,grid_candidate_center=[],[]
    last_seen=0

    for idx,vox in enumerate(non_empty_voxel_keys):
        voxel_grid[tuple(vox)] = crop_points[idx_pts_vox_sorted[last_seen:last_seen+nb_pts_per_voxel[idx]]]
        grid_barycenter.append(np.mean(voxel_grid[tuple(vox)],axis=0))
        grid_candidate_center.append(voxel_grid[tuple(vox)][np.linalg.norm(voxel_grid[tuple(vox)]-np.mean(voxel_grid[tuple(vox)],axis=0),axis=1).argmin()])
        last_seen+=nb_pts_per_voxel[idx]

    return grid_candidate_center

def meshing(input_file, dist, mesh_method, lambert_data, export_obj_path):
    logging.debug(f"Input file : {input_file}")

    points, bbox_percent = get_datas_according_to_file_type(input_file, dist)

    # Get bounding box of all point cloud
    points_min = np.min(points, axis=0)
    points_max = np.max(points, axis=0)
    bbox_size = points_max - points_min
    logging.debug(f"min={points_min}, max={points_max}, size before={bbox_size}")

    mean = np.mean(points, axis=0)
    logging.debug(f"mean={mean}")

    # Get lambert coordinates
    x = lambert_data["latitude"]
    y = lambert_data["longitude"]

    delta = [0, 0, 0]

    # Calculate delta to center point cloud according to mean of all points
    if x > mean[0]:
        delta[0] += abs(x-mean[0])
    else :
        delta[0] -= abs(x-mean[0])

    if y > mean[1]:
        delta[1] += abs(y-mean[1])
    else :
        delta[1] -= abs(y-mean[1])

    # Delta for lidar file from top left
    if input_file.endswith('.copc.laz'):
        mean = mean + delta

    # Crop bounding box and crop point cloud from mean point and bounding box size
    crop_bbox = bbox_size * bbox_percent
    centered_points = points - mean
    logging.debug(f"Points centered after : {centered_points}")

    # Crop points
    crop_points = [p for p in centered_points if abs(p[0]) < crop_bbox[0] and abs(p[1]) < crop_bbox[1]]
    logging.debug(f"Crop points size: {len(crop_points)}")

    # Get x, y and z coordinates from crop_points
    x_all, y_all, z_all = np.hsplit(np.array(crop_points), 3)
    x_all = x_all.flatten()
    y_all = y_all.flatten()
    z_all = z_all.flatten()

    # Center z coordinates
    z_elev = z_all[int(len(z_all)/2)]
    z_all = [p - z_elev for p in z_all]
    z_all = np.array(z_all)

    logging.debug(f"MeshMethod: {mesh_method}")

    # two methods to mesh point cloud
    if mesh_method == "voxel":
        #store coordinates cropped in crop_points
        crop_points = np.column_stack((x_all, y_all, z_all))
        logging.debug(f"Number of points in original file: {len(crop_points)}")

        #change voxel_size to vary subject resolution, it is mesured in meters
        voxel_size=1.5 #determinates the resolution of the mesh
        nb_vox=np.ceil((np.max(crop_points, axis=0) - np.min(crop_points, axis=0))/voxel_size)
        logging.debug(f"The voxel grid is X,Y,Z voxels: {nb_vox}")

        #reduce resolution through the voxel method
        nb_vox_readout = np.prod(nb_vox, dtype=int)
        logging.debug(f"This will reduce number of points to {nb_vox_readout}")

        pts_length = len(crop_points)
        perct = ((1-(nb_vox_readout/pts_length))*100)
        logging.debug(f"Or reduce by {perct}%")

        #grid sampling
        grid_sampled_point_cloud = grid_subsampling(crop_points, voxel_size)
        grid_sample_pc_np = np.array(grid_sampled_point_cloud)

        #Triangulation from voxel grid
        x_all = grid_sample_pc_np[:,0]
        y_all = grid_sample_pc_np[:,1]
        z_all = grid_sample_pc_np[:,2]

    # For both methods, we need to create a mesh
    tris = mtri.Triangulation(x_all, y_all)
    vertices = np.column_stack((x_all, z_all, -y_all))

    # Export mesh
    output_mesh = trimesh.Trimesh(vertices=vertices, faces=tris.triangles)
    output_mesh.export(export_obj_path)
