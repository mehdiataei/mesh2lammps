import trimesh
import numpy as np
import os
import sys
import pandas as pd


atoms = pd.read_csv('../models/'+sys.argv[1], delimiter=' ')
angles = pd.read_csv('../models/'+sys.argv[2], delimiter=' ')

vertices = []
for index, row in atoms.iterrows():
    vertices += [[row['x'], row['y'], row['z']]]
faces = []
for index, row in angles.iterrows():
    faces += [[row['v0'] - 1, row['v1'] - 1, row['v2'] - 1]]

mesh = trimesh.Trimesh(vertices=vertices, faces=faces)

maxz = np.where(mesh.vertices[:,2] == mesh.vertices[:,2].max()) 
minz = np.where(mesh.vertices[:,2] == mesh.vertices[:,2].min()) 

maxy = np.where(mesh.vertices[:,1] == mesh.vertices[:,1].max()) 
miny = np.where(mesh.vertices[:,1] == mesh.vertices[:,1].min()) 

if(mesh.is_watertight):
    print("Volumetric center of mass is set as the origin for the mesh")
    mesh.vertices -= mesh.center_mass

maxx = np.where(mesh.vertices[:,0] == mesh.vertices[:,0].max()) 
minx = np.where(mesh.vertices[:,0] == mesh.vertices[:,0].min())

maxy = np.where(mesh.vertices[:,1] == mesh.vertices[:,1].max()) 
miny = np.where(mesh.vertices[:,1] == mesh.vertices[:,1].min())

maxz = np.where(mesh.vertices[:,2] == mesh.vertices[:,2].max()) 
minz = np.where(mesh.vertices[:,2] == mesh.vertices[:,2].min())

tanXY = np.abs(mesh.vertices[maxx][0][0] - mesh.vertices[minx][0][0] / 2) / np.abs(mesh.vertices[maxx][0][1] - mesh.vertices[minx][0][1] / 2)
tanXZ = np.abs(mesh.vertices[maxz][0][0] - mesh.vertices[minz][0][0] / 2) / np.abs(mesh.vertices[maxz][0][2] - mesh.vertices[minz][0][2] / 2)

rot_matrixXY = trimesh.transformations.rotation_matrix(np.arctan(tanXY) / 2, [0, 0, 1], [0, 0, 0])
rot_matrixXZ = trimesh.transformations.rotation_matrix(np.arctan(tanXZ), [0, 1, 0], [0, 0, 0])

mesh.vertices = trimesh.transformations.transform_points(mesh.vertices, rot_matrixXY)
mesh.vertices = trimesh.transformations.transform_points(mesh.vertices, rot_matrixXZ)

mesh.fix_normals()
mesh.export('centered_mesh.stl')
print("Mesh file is generated!")

mesh.show()