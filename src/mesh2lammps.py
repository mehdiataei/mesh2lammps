import trimesh
import numpy as np
import os
import sys

def main():

    meshName = sys.argv[1]
    mesh = trimesh.load(os.path.join(meshName), process=True)
    mesh.fix_normals()

    if(mesh.is_watertight):
        print("Volumetric center of mass is set as the origin for the mesh")
        mesh.vertices -= mesh.center_mass

    def descriptionLine(description, meshName):

        lines = ["Generation of lammps data from {} mesh file.\n\n".format(meshName)]

        return lines

    def numberLines(num_atoms, num_bonds, num_angles, num_dihedrals, num_impropers):
        lines = ["{} atoms\n".format(num_atoms), "{} bonds\n".format(num_bonds), "{} angles\n".format(num_angles), "{} dihedrals\n".format(num_dihedrals), "{} impropers\n".format(num_impropers), "\n"]
        return lines

    def typesLines(atom_types, bond_types, angle_types, dihedral_types, improper_types):

        lines = ["{} atom types\n".format(atom_types), "{} bond types\n".format(bond_types), "{} angle types\n".format(angle_types), "{} dihedral types\n".format(dihedral_types), "{} improper types\n\n".format(improper_types)]

        return lines

    def domainLines(lx, ly, lz):

        lines = ["{:.2f} {:.2f} xlo xhi\n".format(0.0, lx), "{:.2f} {:.2f} ylo yhi\n".format(0.0, ly), "{:.2f} {:.2f} zlo zhi\n".format(0.0, lz), "\n"]

        return lines

    def massesLines(atoms, masses):
        lines = ["Masses\n\n"]
        for atom, mass in zip(atoms, masses):
            lines += ["{:d} {:.2f}\n".format(atom, mass)]

        lines += ["\n"]

        return lines

    def atomLines(mesh):

        lines = ["Atoms\n\n"]
        for i, vertex in enumerate(mesh.vertices): 
            lines += ["{:d} {:d} {} {:f} {:f} {:f}\n".format(i + 1, 1, 1, vertex[0], vertex[1], vertex[2])]

        lines += ["\n"]

        return lines

    def angleLines(mesh):


        lines = ["Angles\n\n"]
        for i, face in enumerate(mesh.faces):
            lines += ["{:d} {:d} {:d} {:d} {:d}\n".format(i + 1, i + 1, face[0] + 1, face[1] + 1, face[2] + 1)]
        
        lines += ["\n"]

        return lines

    def bondLines(mesh):

        lines = ["Bonds\n\n"]
        for i, edge in enumerate(mesh.face_adjacency_edges):
            lines += ["{:d} {:d} {:d} {:d}\n".format(i + 1, i + 1, edge[0] + 1, edge[1] + 1)]

        lines += ["\n"]

        return lines

    def dihedralLines(mesh):
            lines = ["Dihedrals\n\n"]

            for i, face_adj in enumerate(mesh.face_adjacency):

                face0 = mesh.faces[face_adj[0]]      
                edges = mesh.face_adjacency_edges[i]
                unshared0 = mesh.face_adjacency_unshared[i][0]
                unshared1 = mesh.face_adjacency_unshared[i][1]
                while face0[0] != unshared0:
                    face0 = np.roll(face0, 1)
                face0 = face0.tolist()
                nodes = face0 + [unshared1]

                lines += ["{:d} {:d} {:d} {:d} {:d} {:d}\n".format(i+1, i+1, nodes[0] + 1, nodes[1] + 1, nodes[2] + 1, nodes[3] + 1)]

            lines += ["\n"]
        
            return lines


    def bondCoeffsWLCLines(wlc_coeffs, mesh):
        lines = ["Bond Coeffs\n\n"]

        for i in range(0, mesh.face_adjacency_edges.shape[0]):

            lines += ["{:d} {:f} {:f} {:f} {:f} {:f} {:f} {:f}\n".format(i + 1, wlc_coeffs['kT'], wlc_coeffs['rnorm0'], mesh.edges_unique_length[i] * 2, wlc_coeffs['mu0'], wlc_coeffs['m'], wlc_coeffs['gammaC'], wlc_coeffs['gammaT'])]

        lines += ["\n"]

        return lines

    def angleCoeffsLines(angle_coeffs, mesh):
        lines = ["Angle Coeffs\n\n"]

        for i in range(0, mesh.faces.shape[0]):
            lines += ["{:d} {:f} {:f} {:f} {:f} {:f} {:f} {:f} {:f}\n".format(i + 1, angle_coeffs['Cq'], angle_coeffs['q'], angle_coeffs['ka'], angle_coeffs['Atot0'], angle_coeffs['kv'], angle_coeffs['Vtot0'], angle_coeffs['kd'], mesh.area_faces[i])]

        lines += ["\n"]

        return lines

    def dihedralCoeffsLines(dihedral_coeffs, mesh):
        lines = ["Dihedral Coeffs\n\n"]

        for i in range(0, mesh.face_adjacency_angles.shape[0]):
        
            angle = mesh.face_adjacency_angles[i] * 180 / np.pi
            if (mesh.face_adjacency_convex[i] == False):
                angle = - angle
            
            lines += ["{:d} {:f} {:f}\n".format(i + 1, dihedral_coeffs['kb'], angle)]

        lines += ["\n"]

        return lines

    domain = {'lx': 60, 'ly': 60, 'lz': 60}
    num_atoms = mesh.vertices.shape[0]
    num_angles = mesh.faces.shape[0]
    num_bonds = mesh.edges_unique.shape[0]
    num_dihedrals = mesh.edges_unique.shape[0]

    harmonic_coeffs = {'K_hormonic': 0.01}

    wlc_coeffs = {'kT': 1.100000e-04, 'rnorm0': 0.50000000, 'mu0': 1.000000e-02, 'm': 2.0, 'gammaC': 30.0, 'gammaT': 90.0}

    angle_coeffs = {'Cq': 0.0, 'q': 1.0, \
    'ka': 0.0075, 'Atot0': mesh.area, 'kv': 0.0966, 'Vtot0': mesh.volume, 'kd': 0.367}

    dihedral_coeffs = {'kb': 1.330000e-02}

    # Center mesh
    center_mass_loc = np.array([domain['lx'], domain['ly'], domain['lz']]) / 2
    mesh.vertices += center_mass_loc

    print("The mesh has {} atoms, {} angles, {} bonds, and {} dihedrals".format(num_atoms, num_angles, num_bonds, num_dihedrals))

    datafile = open("mesh.data","w") 

    lines = []

    lines += descriptionLine("mesh generated by mesh2lammps", meshName)
    lines += numberLines(num_atoms, num_bonds, num_angles, num_dihedrals, 0)

    lines += typesLines(1, num_bonds, num_angles, num_dihedrals, 0)
    lines += domainLines(domain['lx'], domain['ly'], domain['lz'])
    lines += massesLines([1], [1.000])
    lines += atomLines(mesh)
    lines += bondLines(mesh)
    lines += angleLines(mesh)
    lines += dihedralLines(mesh)
    lines += bondCoeffsWLCLines(wlc_coeffs, mesh)
    lines += angleCoeffsLines(angle_coeffs, mesh)
    lines += dihedralCoeffsLines(dihedral_coeffs, mesh)

    datafile.writelines(lines)
    datafile.close()

    print("Lammps data file is generated!")

    mesh.show()