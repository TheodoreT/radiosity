import numpy as np
import os
import copy
import multiprocessing
from utils import Isocell
from utils import LightDistributionCurve
from utils import FormFactor

from scipy.io import loadmat

import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')

import pyvista as pv
import open3d as o3d
import trimesh
import vtkplotter as vp

from numba import jit, cuda

def plot_mesh(verts, faces):
    # points = isocell.points
    # cell_points = np.column_stack([isocell.Xc, isocell.Yc, isocell.Zc])
    poly = pv.PolyData(verts, faces)
    # cell = pv.PolyData(cell_points)
    # # lines = pv.lines_from_points(cell.points)
    #
    plotter = pv.BackgroundPlotter()
    plotter.add_mesh(poly, show_edges=True)
    # # plotter.add_mesh(cell, color="blue", point_size=1)
    # # plotter.add_mesh(lines, color='blue')
    plotter.add_axes()
    plotter.show()
    plotter.app.exec_()


def test_formfactors():
    # load data from a .mat file
    data = loadmat('../cad_models/subdivided/cadModel_garchingVisionLab.mat')

    # manual retrieval (TODO: check if this can be handled automatically somehow)
    faces = data['cadModel_'][0][0][0] - 1
    # faces = np.insert(faces, 0, 3, axis=1)
    # vertices = np.vstack([[0,0,0], data['cadModel_'][0][0][1]])
    vertices = data['cadModel_'][0][0][1]
    floor_patches = data['cadModel_'][0][0][2] - 1
    ceiling_patches = data['cadModel_'][0][0][3] - 1
    wall_patches = data['cadModel_'][0][0][4][0][0][4] - 1
    light1_patches = data['cadModel_'][0][0][5][0][0][0] - 1
    light2_patches = data['cadModel_'][0][0][5][0][0][1] - 1
    light3_patches = data['cadModel_'][0][0][5][0][0][2] - 1
    light4_patches = data['cadModel_'][0][0][5][0][0][3] - 1
    light5_patches = data['cadModel_'][0][0][5][0][0][4] - 1
    light6_patches = data['cadModel_'][0][0][5][0][0][5] - 1
    light7_patches = data['cadModel_'][0][0][5][0][0][6] - 1
    light8_patches = data['cadModel_'][0][0][5][0][0][7] - 1
    light_patches = data['cadModel_'][0][0][5][0][0][8] - 1
    desk_patches = data['cadModel_'][0][0][6][0][0][8] - 1
    leg_desk_patches = data['cadModel_'][0][0][7] - 1
    panel_patches = data['cadModel_'][0][0][8] - 1
    panel_handle_patches = data['cadModel_'][0][0][9] - 1
    centroids = data['cadModel_'][0][0][10]
    normals = data['cadModel_'][0][0][11]
    areas = data['cadModel_'][0][0][12]

    # proc = multiprocessing.Process(target=plot_mesh, args=(vertices, faces[np.vstack([floor_patches, wall_patches, desk_patches, leg_desk_patches, panel_patches, panel_handle_patches, light_patches]),:].reshape(-1,4),))
    # proc.daemon = False
    # proc.start()
    # # faces = np.insert(faces, 0, 3, axis=1)
    # # # plot_mesh(vertices, faces)
    # # plot_mesh(vertices, faces[np.vstack([floor_patches, wall_patches, desk_patches, leg_desk_patches, panel_patches, panel_handle_patches, light_patches]),:].reshape(-1,4))

    # # open3d + point cloud example
    # pcd = o3d.geometry.PointCloud()
    # pcd.points = o3d.utility.Vector3dVector(np.asarray(vertices))
    #
    # pcd.estimate_normals()
    # o3d.visualization.draw_geometries([pcd])

    # open3d + mesh example
    # # mesh = o3d.geometry.TriangleMesh(vertices=np.asarray(vertices), faces=faces)
    # mesh = o3d.geometry.TriangleMesh()
    # mesh.vertices = o3d.utility.Vector3dVector(vertices)
    # mesh.triangles = o3d.utility.Vector3iVector(faces)
    # # mesh.triangles = o3d.utility.Vector3iVector(faces[np.vstack([floor_patches, wall_patches, desk_patches, leg_desk_patches, panel_patches, panel_handle_patches, light_patches]),:].reshape(-1,3))
    # mesh.triangle_normals = o3d.utility.Vector3dVector(normals)
    # o3d.visualization.draw_geometries([mesh])

    # mesh = pv.PolyData(vertices, faces)
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, face_normals=normals, process=False, use_embree=True)
    # vp.show(vp.trimesh2vtk(mesh).alpha(0.1).lw(0.1), axes=4)

    # ff = FormFactor(mesh)
    # ffs = FormFactor(mesh).calculate_form_factor(processes=5)
    ffs = FormFactor(mesh).calculate_form_factor(processes=multiprocessing.cpu_count() - 1)

    print('End testing the form factors module!!!!')
    # plt.show()

# function optimized to run on gpu
@jit(target ="cuda")
def func2(a):
    for i in range(10000000):
        a[i]+= 1



if __name__ == '__main__':
    print('Testing the formfactors module!!!!')
    # test_formfactors()
    n = 10000000
    a = np.ones(n, dtype=np.float64)
    b = np.ones(n, dtype=np.float32)

    func2(a)
    os._exit(0)