![Cover Photo of a mesh and lammmps structure](imgs/CoverPhoto.png)
# Mesh2Lammps
Mesh2Lammps is an open-source software to convert triangular unstructured meshes to course-grained LAMMPS molecular input files.

# Installation
You can perform a minimal install of Mesh2Lammps with:

```
$ git clone https://github.com/mehdiataei/mesh2lammps
$ cd mesh2lammps
$ python setup.py install 

```
If you prefer, you can do a minimal install of the packaged version directly from PyPI:

```
pip install mesh2lammps 

```
## Run an example

First, close the repository using the following git command:

```
$ git clone https://github.com/mehdiataei/LBfoam.git
```


Converting LAMMPS input file to mesh data and vice versa for the `RBC` example:
```
$ cd samples/RBC/

```

In this directory there is a mesh file `rbc.stl`. To generate the LAMMPS input:
```
$ mesh2lammps rbc.stl

```
Now, ` mesh.data ` fiile is generated which can be used as LAMMPS input data.

Likewise, you can generate the mesh file from the LAMMPS input file including `rbc_atoms.csv` and `rbc_faces.csv`. To do this:
```
$ lammps2mesh rbc_atoms.csv rbc_faces.csv

```
Now, you have created the `rbc.stl` mesh file.


![Red-blood cell example](imgs/RBCExample.png)

## Getting help and bug report

Please submit an issue if you found a bug in the program or needed help with the software.